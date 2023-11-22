from nltk.sentiment import SentimentIntensityAnalyzer
from newspaper import Article
from colorama import init, Fore
import yfinance as yf
import pandas as pd
import nltk

nltk.download('vader_lexicon')
nltk.download('punkt')

init(autoreset=True)


def get_news():
    top30 = pd.read_csv('data/30_data.csv')
    tickers = top30['Symbol']

    average_sentiments = {}  # To store average sentiment for each stock

    for stock_ticker in tickers:
        print(f'{Fore.CYAN}[Stock] {Fore.GREEN}{stock_ticker} selected{Fore.RESET}')
        print(f'{Fore.CYAN}[{stock_ticker}] {Fore.YELLOW}Fetching news...{Fore.RESET}')

        try:
            stock = yf.Ticker(stock_ticker)
            
            stock_news = stock.news

            total_sentiment = 0
            num_headlines = 0

            for news_item in stock_news:
                headline_content = news_item['title']
                headline_url = news_item.get('url') or news_item.get('link', 'URL not available')
                headline_ticker = stock_ticker

                sentiment_score = analyse_headlines(headline_content, headline_url, headline_ticker)
                total_sentiment += sentiment_score
                num_headlines += 1

                # Save sentiment to file after each news item
                with open('sentiment.txt', 'a') as f:
                    if sentiment_score >= 0.5:
                        f.write(f"[{stock_ticker}] Possible positive lead stock [{sentiment_score:.4f}]\n")
                        f.write(f"[{stock_ticker}] {headline_content} | {headline_url} \n\n")
                    elif sentiment_score <= -0.5:
                        f.write(f"[{stock_ticker}] Possible negative lead stock [{sentiment_score:.4f}]\n")
                        f.write(f"[{stock_ticker}] {headline_content} | {headline_url} \n\n")
                    else:
                        # f.write(f"[{stock_ticker}] Neutral Stock [{sentiment_score:.4f}]\n")
                        f.write(f"")

            if num_headlines > 0:
                average_sentiment = total_sentiment / num_headlines
                average_sentiments[stock_ticker] = average_sentiment

        except ValueError:
            print(f'{Fore.CYAN}[{stock_ticker}] {Fore.RED}Error fetching stock. Rate limit reached.{Fore.RESET}')

    # Write average sentiments to 'sentiment.txt'
    with open('sentiment.txt', 'a') as f:
        for stock_ticker, average_sentiment in average_sentiments.items():
            if average_sentiment >= 0.5:
                f.write(f"[{stock_ticker}] Possible positive lead stock [{average_sentiment:.4f}]\n")
            elif average_sentiment <= -0.5:
                f.write(f"[{stock_ticker}] Possible negative lead stock [{average_sentiment:.4f}]\n")
            else:
                f.write(f"[{stock_ticker}] Neutral Stock [{average_sentiment:.4f}]\n")


def analyse_headlines(headline_content, headline_url, headline_ticker, sensitivity=1.0):
    sia = SentimentIntensityAnalyzer()

    sentiment_score = sia.polarity_scores(headline_content)['compound']
    sentiment_score *= sensitivity

    article = Article(headline_url)
    article.download()
    article.parse()
    article.nlp()
    date = (article.publish_date)
    keywords = (article.keywords)

    article_score = sia.polarity_scores(article.text)['compound']

    if sentiment_score >= 0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.GREEN}Positive')
    elif sentiment_score <= -0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.RED}Negative')
    else:
        print(f'{Fore.CYAN}[Sentiment] {Fore.YELLOW}Neutral for Headline ({headline_content})')
        print(f'{Fore.RED}[=================================================================]')
        return 0  # Return 0 for neutral sentiment

    print(f'{Fore.YELLOW}[Analysis for Headline]')
    print(f'{Fore.YELLOW}[Headline]{Fore.RESET} {headline_content}')
    print(f'{Fore.YELLOW}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.YELLOW}[URL]{Fore.RESET} {headline_url}')
    print(f'{Fore.YELLOW}[Sentiment Score]{Fore.RESET} {sentiment_score:.4f}')

    print('----------')

    print(f'{Fore.CYAN}[Analysis for Article]')
    print(f'{Fore.CYAN}[Keywords]{Fore.RESET} {keywords}')
    print(f'{Fore.CYAN}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.CYAN}[Date Published]{Fore.RESET} {date}')
    print(f'{Fore.CYAN}[Sentiment Score]{Fore.RESET} {article_score:.4f}')

    print(f'{Fore.RED}[=================================================================]')
    return sentiment_score

if __name__ == "__main__":
    devmode = False
    get_news()
