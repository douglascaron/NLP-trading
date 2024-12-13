# IMPORTS
import yfinance as yf
import pandas as pd

# Read the top 30 stock data from a CSV file
top30 = pd.read_csv('30_data.csv')
tickers = top30['Symbol']
average_sentiments = {}

# Loop through each stock ticker
for stock_ticker in tickers:
    print(f'[Stock] {stock_ticker} selected')
    print(f'[{stock_ticker}] Fetching news...')
    
    # Fetch stock news using yfinance
    stock = yf.Ticker(stock_ticker)
    stock_news = stock.news
    
    # Print each news item's title and ticker
    for news_item in stock_news:
        print(f"TITLE: {news_item['title']}")
        print(f"TICKER: {stock_ticker}")
        print("------------------------------------------------")

# Unit tests
def test_read_csv():
    print("Testing CSV reading...")
    df = pd.read_csv('30_data.csv')
    assert not df.empty, "CSV file is empty"
    assert 'Symbol' in df.columns, "CSV file does not contain 'Symbol' column"
    print("✔️ test_read_csv passed")

def test_fetch_news():
    print("Testing news fetching...")
    stock = yf.Ticker('AAPL')
    stock_news = stock.news
    assert isinstance(stock_news, list), "News is not a list"
    if stock_news:
        assert 'title' in stock_news[0], "News item does not contain 'title'"
    print("✔️ test_fetch_news passed")

# Run tests
if __name__ == "__main__":
    tests = [test_read_csv, test_fetch_news]
    for test in tests:
        test()
    print("All tests passed.")
