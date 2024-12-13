# IMPORTS
import time
import requests as request
import yfinance as yf
import pandas as pd


top30 = pd.read_csv('30_data.csv')
tickers = top30['Symbol']
average_sentiments = {}

for stock_ticker in tickers:
    print(f'[Stock] {stock_ticker} selected')
    print(f'[{stock_ticker}] Fetching news...')
    stock = yf.Ticker(stock_ticker)
    stock_news = stock.news
    for news_item in stock_news:
        print(f"TITLE: {news_item['title']}")
        print(f"TICKER: {stock_ticker}")
        print("------------------------------------------------")
    input()




# VARIABLES
api_endpoint = "https://newsapi.org/v2/everything" 
news_api_key = "34f0ee4c5a904613a92030e76108e78b"

# FUNCTIONS
def fetch_news(api_endpoint, keywords, interval):
    news_articles = []
    while True:
        try:
            response = request.get(api_endpoint, params={'q': keywords, 'interval': interval})
            if response.status_code == 200:
                data = response.json()
                articles = response.json().get('articles', [])
                for article in articles:
                    news_article = {
                        "title": article["title"],
                        "content": article["content"],
                        "timestamp": article["publishedAt"]}
                    news_articles.append(news_article)
            else:
                print("Failed to fetch news data, status: ", response.status_code)
        except request.exceptions.RequestException as e:
            print("Network error: ", e)
            time.sleep(interval)



# MAIN


