import requests

_BASE_URL_ = "https://query2.finance.yahoo.com"

def api_request_news(ticker):
    url = f"{_BASE_URL_}/v1/finance/search?q={ticker}"

    # Making the API request
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error making API request: {e}")

    data = response.json()

    if "Will be right back" in data.get("error", ""):
        raise RuntimeError("*** YAHOO! FINANCE IS CURRENTLY DOWN! ***\n"
                            "Our engineers are working quickly to resolve "
                            "the issue. Thank you for your patience.")

    news = data.get("news", [])
    return news

ticker_symbol = "AAPL"
try:
    news_data = api_request_news(ticker_symbol)
    print(news_data)
except RuntimeError as e:
    print(e)

# import yfinance as yf

# stock = yf.Ticker("AAPL")
# hist = stock.history(period="1d")

# print(stock.news)