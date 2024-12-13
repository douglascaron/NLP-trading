from nltk.sentiment import SentimentIntensityAnalyzer
from newspaper import Article
from colorama import init, Fore
import yfinance as yf

init(autoreset=True)

def get_news():
    stock_ticker = input(f'{Fore.CYAN}[Stock] Please pick a stock (E.G: MSFT): {Fore.RESET}')
    print(f'{Fore.CYAN}[Stock] {Fore.GREEN}{stock_ticker} selected{Fore.RESET}')
    print(f'{Fore.CYAN}[{stock_ticker}] {Fore.YELLOW}Fetching news...{Fore.RESET}')

    try:
        stock = yf.Ticker(stock_ticker)
        stock_news = stock.news
        for news_item in stock_news:
            headline_content = news_item['title']
            headline_url = news_item.get('url') or news_item.get('link', 'URL not available')
            headline_ticker = stock_ticker
            analyse_headlines(headline_content, headline_url, headline_ticker)
    
    except ValueError:
        print(f'{Fore.CYAN}[{stock_ticker}] {Fore.RED}Error fetching stock. Please make sure this is a valid ticker.{Fore.RESET}')


def analyse_headlines(headline_content, headline_url, headline_ticker, sensitivity=1.0):
    sia = SentimentIntensityAnalyzer()

    sentiment_score = sia.polarity_scores(headline_content)['compound']
    sentiment_score *= sensitivity

    if sentiment_score >= 0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.GREEN}Positive')
    elif sentiment_score <= -0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.RED}Negative')
    else:
        print(f'{Fore.CYAN}[Sentiment] {Fore.YELLOW}Neutral for Headline ({headline_content})')
        print("------------------------------------------------")
        return 0  # Return 0 for neutral sentiment

    print(f'{Fore.YELLOW}[Analysis for Headline]')
    print(f'{Fore.YELLOW}[Headline]{Fore.RESET} {headline_content}')
    print(f'{Fore.YELLOW}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.YELLOW}[URL]{Fore.RESET} {headline_url}')
    print(f'{Fore.YELLOW}[Sentiment Score]{Fore.RESET} {sentiment_score:.4f}')

    print("------------------------------------------------")
    return sentiment_score

if __name__ == "__main__":
    devmode = False
    get_news()