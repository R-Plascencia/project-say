from interests.models import Interest
from .models import NewsItem
from .models import NewsResult
from django.utils import timezone
from django.utils.html import strip_tags
from newspaper import Article
import feedparser
import re



# Dictionary of all allowed RSS sources of news
rss_sources = {'AP': 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',
    'Reuters - Politics': 'http://feeds.reuters.com/Reuters/PoliticsNews',
    'Reuters - Domestic': 'http://feeds.reuters.com/Reuters/domesticNews',
    'The Economist - United States': 'http://www.economist.com/sections/united-states/rss.xml',
    'The Economist - Economics': 'http://www.economist.com/sections/economics/rss.xml',
    'The Independent': 'http://www.independent.co.uk/news/world/americas/rss',
    'BBC': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
    'WSJ': 'http://www.wsj.com/xml/rss/3_7085.xml',
    'Amnesty International': 'http://www.amnestyusa.org/rss/news/Americas/rss.xml'
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
Called from the Interest:Create view (for now). Takes the interest's keywords and searches each
RSS source for word matches in their titles and desctiptions. If match is found, create NewsItem
with the article's information and add to the 'results' dictionary. This will then be attached
to the Interest's news results

Returns: results - dictionary
'''
def build_results(request, interest):
    results = NewsResult(interest=interest)
    result_found = False
    enough_matches = False

    # Get the keywords associated with Interest
    keywords = interest.keywords.split(',')
    keyword_count = len(keywords)

    # Bring in the parsed feeds from each RSS source
    knowledge_sources = parse_rss_sources()

    # For every source and its parsed entries
    for source, entries in knowledge_sources.items():
        # There are multiple stories in each "entry"
        for story in entries:
            description = story.description.encode('utf-8')
            description = str(description)
            description = strip_tags(description)
            title = story.title
            link = story.link

            # Use newspaper to parse the article into useful pieces
            article = Article(link)
            article.download()
            article.parse()

            # Find the keywords in the article's text (or in the desc if somehow newspaper doesn't succeed
            # in getting the text back)
            if article.text == '' or article.text == None:
                keywords_found = find_keywords(description)
            else:
                text = article.text.encode('utf-8')
                keywords_found = find_keywords(str(text))
            print(keywords_found)
            return None

            # Search for the associated Interest keywords in the desctiptions and titles of every story
            matches = 0
            for word in keywords:
                word = word.lower()
                # If something is found, raise the flag
                if re.search(r'\b' + word + r'\b', description.lower()) or re.search(r'\b' + word + r'\b', title.lower()):
                    # print('{0} found'.format(word))
                    result_found = True
                    matches += 1

            if keyword_count > 1:
                if matches >= 2: enough_matches = True
            else:
                if matches == 1: enough_matches = True

            # Before moving on to next thing, create a news item and add it to the results then reset flags
            if result_found and enough_matches:
                interest.last_refreshed = timezone.now()
                interest.save()
                news_item = NewsItem()
                news_item.title = title
                news_item.link = link
                news_item.descr = description
                news_item.source = source
                news_item.save()
                results.save()
                results.newsitems.add(news_item)
                results.save()
                result_found = False
                enough_matches = False
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

    aux = [(kw_dict[key], key) for key in kw_dict]
    aux.sort()
    aux.reverse()
    topword_list = []
    for i in range(n):
        topword_list.append(aux[i][1])

    return topword_list
