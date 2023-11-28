import feedparser,nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def api_news(symbol):
    RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
    feed_url = RSS_URL + symbol
    feed = feedparser.parse(feed_url)
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
    sentiment = (SentimentIntensityAnalyzer().polarity_scores(item['title'])['compound'])
    if sentiment > 0:
        print(f"[{symbol}] Positive [{sentiment:.4f}]\n")
    elif sentiment < -0:
        print(f"[{symbol}] Negative [{sentiment:.4f}]\n")
    else:
        print(f"[{symbol}] Neutral [{sentiment:.4f}]\n")
    print("\n")