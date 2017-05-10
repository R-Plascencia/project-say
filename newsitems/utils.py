from interests.models import Interest
from .models import NewsItem
from .models import NewsResult
from django.utils import timezone
from django.utils.html import strip_tags
from django.db import IntegrityError
from newspaper import Article
from datetime import datetime
import feedparser


# Dictionary of all allowed RSS sources of news
rss_sources = {'AP': 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',
    'Reuters - Politics': 'http://feeds.reuters.com/Reuters/PoliticsNews',
    'Reuters - Domestic': 'http://feeds.reuters.com/Reuters/domesticNews',
    'The Economist - United States': 'http://www.economist.com/sections/united-states/rss.xml',
    'The Economist - Economics': 'http://www.economist.com/sections/economics/rss.xml',
    'The Independent': 'http://www.independent.co.uk/news/world/americas/rss',
    'BBC': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
    'WSJ': 'http://www.wsj.com/xml/rss/3_7085.xml',
}

# English stopwords that we don't care about
cachedStopWords = [
'i',
'me',
'my',
'myself',
'we',
'our',
'ours',
'ourselves',
'you',
'your',
'yours',
'yourself',
'yourselves',
'he',
'him',
'his',
'himself',
'she',
'her',
'hers',
'herself',
'it',
'its',
'itself',
'they',
'them',
'their',
'theirs',
'themselves',
'what',
'which',
'who',
'whom',
'this',
'that',
'these',
'those',
'am',
'is',
'are',
'was',
'were',
'be',
'been',
'being',
'have',
'has',
'had',
'having',
'do',
'does',
'did',
'doing',
'a',
'an',
'the',
'and',
'but',
'if',
'or',
'because',
'as',
'until',
'while',
'of',
'at',
'by',
'for',
'with',
'about',
'against',
'between',
'into',
'through',
'during',
'before',
'after',
'above',
'below',
'to',
'from',
'up',
'down',
'in',
'out',
'on',
'off',
'over',
'under',
'again',
'further',
'then',
'once',
'here',
'there',
'when',
'where',
'why',
'how',
'all',
'any',
'both',
'each',
'few',
'more',
'most',
'other',
'some',
'such',
'no',
'nor',
'not',
'only',
'own',
'same',
'so',
'than',
'too',
'very',
'can',
'will',
'just',
'don',
'should',
'would',
'now',
'whether',
'-',
]


'''
Helper function that takes all the sources and RSS links in the rss_sources dictionary and
creates a new dictionary with the source and its parsed data

Returns: parsed_feeds - dictionary
'''
def parse_rss_sources():
    parsed_feeds = dict()
    for source,link in rss_sources.items():
        feed = feedparser.parse(link)
        parsed_feeds.update({source: feed.entries})
    return parsed_feeds


'''
Builds up the newsitems in the DB. Parses each RSS source, iterates through the articles in the
feed and finds the keywords for each. Then creates entry in DB

Returns - nothing
'''
def populate_newsitems():
    knowledge_sources = parse_rss_sources()

    # Keep a list of what we're saving to avoid dups
    stories_saved = []

    # For every source and its parsed entries
    for source, entries in knowledge_sources.items():
        # There are multiple stories in each "entry"
        for story in entries:
            title = story.title

            # Ensure there are no duplicate stories
            if title in stories_saved:
                continue
            else:
                stories_saved.append(title)

            description = story.description.encode('utf-8')
            description = str(description)
            description = strip_tags(description)
            link = story.link

            # Make the date into something that can be converted into datetime objects
            publish_date = story.published_parsed
            date = []
            for i in publish_date:
                date.append(str(i))
            publish_date = '-'.join(date[:3])
            publish_date = datetime.strptime(publish_date, '%Y-%m-%d')

            # Use newspaper to parse the article into useful pieces
            article = Article(link)
            article.download()
            article.parse()

            # Find the keywords in the article's text (or in the desc if somehow newspaper doesn't succeed
            # in getting the text back)
            if article.text == '' or article.text == None:
                keywords_found = find_keywords(description)
            else:
                text = article.text
                keywords_found = find_keywords(str(text))

            # Create NewsItem and Save into DB unless it raises IntegrityError (already exists)
            news_item = NewsItem()
            try:
                news_item.title = title
                news_item.save()
            except IntegrityError as e:
                continue
            news_item.link = link
            news_item.description = description
            news_item.source = source
            news_item.top_img = article.top_image
            news_item.pub_date = publish_date
            news_item.keywords = keywords_found
            news_item.save()
            print("Newsitem {} saved".format(title))

    # Not sure what else to return here, since seems like Celery tasks need to return something
    # return True


'''
Takes the keywords of the Interest passed in and compares with the keywords of NewsItems
in the database. If match is found, add that NewsItem into the Interest's NewsResults
and save

Returns - results dictionary
'''
def get_newsitems(request, interest):
    results = NewsResult(interest=interest)
    result_found = False

    # Get the keywords associated with Interest
    keywords = interest.keywords.split(',')

    # Bring in all NewsItems (better way?)
    queryset = NewsItem.objects.all()#.order_by('-pub_date')

    # Search for the associated Interest keywords for each NewsItem
    for news_item in queryset:
        for word in keywords:
            word = word.strip().lower()
            # If something is found, raise the flag
            if word in news_item.keywords:
                print("Found result {}".format(word))
                result_found = True

        # If something found, update the Interest and add Newsitem to the results
        if result_found:
            interest.last_refreshed = timezone.now()
            interest.save()
            results.save()
            results.newsitems.add(news_item)
            results.save()
            result_found = False

    return results


'''
Finds keywords for a given block of text, creates a dictionary with the words and their frequency,
converts this into a list of tuples containing (count, word), then iterates through the top n
items in the list and returns the word portion of the tuple

Returns: keywords list with top n keywords (defaults at 5)
'''
def find_keywords(text, n=5):
    text = ' '.join([word for word in text.split() if word not in cachedStopWords])
    wordlist = text.split()
    word_freq = [wordlist.count(p) for p in wordlist]
    kw_dict = dict(zip(wordlist, word_freq))

    kw_list = [(kw_dict[key], key) for key in kw_dict]
    kw_list.sort()
    kw_list.reverse()
    topword_list = []
    for i in range(n):
        try:
            topword_list.append(kw_list[i][1].lower())
        except IndexError:
            pass

    return topword_list
