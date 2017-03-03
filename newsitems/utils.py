from interests.models import Interest
from .models import NewsItem
from .models import NewsResult
from django.utils import timezone
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

    # Get the keywords associated with Interest
    keywords = interest.keywords.split(',')

    # Bring in the parsed feeds from each RSS source
    knowledge_sources = parse_rss_sources()

    # For every source and its parsed entries
    for source, entries in knowledge_sources.items():
        # There are multiple stories in each "entry"
        for story in entries:
            description = story.description.encode('utf-8')
            description = str(description)
            description = description.split('<div', 1)[0]
            title = story.title
            link = story.link

            # Search for the associated Interest keywords in the desctiptions and titles of every story
            for word in keywords:
                word = word.lower()
                # If something is found, raise the flag
                if re.search(r'\b' + word + r'\b', description.lower()) or re.search(r'\b' + word + r'\b', title.lower()):
                    # print('{0} found'.format(word))
                    result_found = True

            # Before moving on to next thing, create a news item and add it to the results then reset flag
            if result_found:
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
    return results
