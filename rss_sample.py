import feedparser
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np


finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
labels = {0:f'[Sentiment] Neutral', 1:f'[Sentiment] Positive',2:f'[Sentiment] Negative'}

def analyze_sentiment(data):
    inputs = tokenizer(data, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Ensure the input tensors have the correct size
    for key in inputs:
        inputs[key] = inputs[key][:, :512]  # Truncate if necessary
    analysis = finbert(**inputs)[0]
    for idx, sent in enumerate(analysis):
        # print(sent, '----', labels[np.argmax(analysis.detach().numpy()[idx])])
        sentiment = labels[np.argmax(analysis.detach().numpy()[idx])]
    return sentiment

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

symbol = 'AAPL'
news = api_news(symbol)
for item in news:
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    print(f"Published: {item['published']}")
    sentiment = analyze_sentiment(item['title'])
    print(sentiment)
    print("\n")