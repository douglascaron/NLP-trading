from newspaper import Article
from colorama import init, Fore
import yfinance as yf
import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import os

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
labels = {0:f'{Fore.CYAN}[Sentiment] {Fore.YELLOW}Neutral', 1:f'{Fore.CYAN}[Sentiment] {Fore.GREEN}Positive',2:f'{Fore.CYAN}[Sentiment] {Fore.RED}Negative'}
init(autoreset=True)

if os.path.exists("sentiment.txt"):
    os.remove("sentiment.txt")

def analyze_sentiment(data):
    inputs = tokenizer(data, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Ensure the input tensors have the correct size
    for key in inputs:
        inputs[key] = inputs[key][:, :512]  # Truncate if necessary
    analysis = finbert(**inputs)[0]
    
    # Assuming FinBERT outputs a tensor with sentiment scores
    sentiment_score = analysis.detach().numpy()

    print(analysis)
    print(f'Sentiment Score: {sentiment_score}')

    return sentiment_score


def get_news():
    top30 = pd.read_csv('data/30_data.csv')
    tickers = top30['Symbol']

    average_sentiments = {}

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

    with open('sentiment.txt', 'a') as f:
        for stock_ticker, average_sentiment in average_sentiments.items():
            if average_sentiment >= 0.5:
                f.write(f"[{stock_ticker}] Possible positive lead stock [{average_sentiment:.4f}]\n")
            elif average_sentiment <= -0.5:
                f.write(f"[{stock_ticker}] Possible negative lead stock [{average_sentiment:.4f}]\n")
            else:
                f.write(f"[{stock_ticker}] Neutral Stock [{average_sentiment:.4f}]\n")


def analyse_headlines(headline_content, headline_url, headline_ticker):
    sentiment_score = analyze_sentiment(headline_content)

    article = Article(headline_url)
    article.download()
    article.parse()
    article.nlp()
    date = (article.publish_date)

    article_score = analyze_sentiment(article.text)

    print(f'{Fore.YELLOW}[Analysis for Headline]')
    print(f'{Fore.YELLOW}[Headline]{Fore.RESET} {headline_content}')
    print(f'{Fore.YELLOW}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.YELLOW}[URL]{Fore.RESET} {headline_url}')
    print(f'{Fore.YELLOW}[Sentiment Score]{Fore.RESET} {sentiment_score:.4f}')

    print('----------')

    print(f'{Fore.CYAN}[Analysis for Article]')
    print(f'{Fore.CYAN}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.CYAN}[Date Published]{Fore.RESET} {date}')
    print(f'{Fore.CYAN}[Sentiment Score]{Fore.RESET} {article_score:.4f}')

    print(f'{Fore.RED}[=================================================================]')
    return sentiment_score

if __name__ == "__main__":
    devmode = False
    get_news()
