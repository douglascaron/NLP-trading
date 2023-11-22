from nltk.sentiment import SentimentIntensityAnalyzer
from newspaper import Article, ArticleException
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from colorama import init, Fore

init(autoreset=True)

def get_headlines():
    try:
        url = 'https://seekingalpha.com/market-news'
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} Using User-Agent: {headers["User-Agent"]}')

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} Request successful!')

        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} HTML parsed successfully!')

        headline_elements = soup.find_all('a', class_="text-share-text")
        print(f'{Fore.BLUE}[✔]{Fore.WHITE} Headlines found successfully!')
        print("------")

        headlines = []

        for element in headline_elements:
            headline_text = element.text.strip()
            headline_url = 'https://seekingalpha.com' + element['href']

            footer = element.find_next('footer')
            ticker_element = footer.find('a', class_='mw_N')
            if ticker_element:
                ticker_symbol = ticker_element.find('span', class_='mw_Fv').text.strip()
            else:
                ticker_symbol = "N/A"

            headlines.append({
                'headline': headline_text,
                'url': headline_url,
                'ticker_symbol': ticker_symbol,
            })

        return headlines

    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}[✖] Error: {e}')
        return None


def analyze_article(headline_url):
    article_div_class = "ml_E2 q_8 q_as q_aQ q_6"  # Replace this with the actual class name

    try:
        response = requests.get(headline_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article_div = soup.find('div', {'class': article_div_class})
        print(article_div)
        if article_div:
            article_text = ""
            paragraphs = article_div.find_all('p')
            for paragraph in paragraphs:
                article_text += paragraph.get_text() + "\n"

            article = Article(headline_url)
            article.set_text(article_text)
            article.download()
            article.parse()
            article.nlp()

            blob = TextBlob(article.text)
            news_sentiment = blob.sentiment.polarity

            if news_sentiment >= 0.1:
                news_sentiment_label = f'{Fore.GREEN}positive{Fore.RESET}'
            elif news_sentiment <= -0.1:
                news_sentiment_label = f'{Fore.RED}negative{Fore.RESET}'
            else:
                news_sentiment_label = f'{Fore.RESET}neutral'
            print(f"{Fore.CYAN}[Article Summary Sentiment] {news_sentiment_label}")
            print(f"{Fore.YELLOW}[Article Summary] {Fore.WHITE}{article.summary}")
        else:
            print(f"{Fore.RED}[✖] [ERROR]: Article contents not found - this may be due to rate limiting.")

    except requests.RequestException as request_error:
        print(f'{Fore.RED}[✖] [REQUEST ERROR]: {request_error}')
    except Exception as error:
        print(f'{Fore.RED}[✖] [ERROR]: {error}')

def analyse_headlines(headline_content, headline_url, headline_ticker, sensitivity=1.0):
    sia = SentimentIntensityAnalyzer()

    sentiment_score = sia.polarity_scores(headline_content)['compound']
    sentiment_score *= sensitivity

    if sentiment_score >= 0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.GREEN}Positive')
    elif sentiment_score <= -0.05:
        print(f'{Fore.CYAN}[Sentiment] {Fore.RED}Negative')
    else:
        print(f'[Sentiment] {Fore.YELLOW}Neutral for Headline ({headline_content})')
        print("------------------------------------------------")
        return 0  # Return 0 for neutral sentiment

    print(f'{Fore.YELLOW}[Analysis for Headline]')
    print(f'{Fore.YELLOW}[Headline]{Fore.RESET} {headline_content}')
    print(f'{Fore.YELLOW}[Ticker]{Fore.RESET} {headline_ticker}')
    print(f'{Fore.YELLOW}[Sentiment Score]{Fore.RESET} {sentiment_score:.4f}')

    print("------")

    analyze_article(headline_url)

    print("------------------------------------------------")
    return sentiment_score


if __name__ == "__main__":
    devmode = False
    headlines = get_headlines()

    for i, news_item in enumerate(headlines, start=1):
        headline_content = news_item['headline']
        headline_url = news_item['url']
        headline_ticker = news_item['ticker_symbol']
        sensitivity = 1.0  # shift from -1 to 1
        sentiment_score = analyse_headlines(headline_content, headline_url, headline_ticker, sensitivity)
        
        if devmode and sentiment_score != 0:
            break  