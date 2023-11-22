import feedparser
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def api_news(symbol):
    RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
    feed_url = RSS_URL + symbol
    feed = feedparser.parse(feed_url)

    # Extract news items from the feed
    news = []
    for entry in feed.entries:
        news_item = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        }
        news.append(news_item)

    return news

symbol = 'AMAT'
news = api_news(symbol)
for item in news:
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    print(f"Published: {item['published']}")
    print(SentimentIntensityAnalyzer().polarity_scores(item['title'])['compound'])
    print("\n\n\n")

