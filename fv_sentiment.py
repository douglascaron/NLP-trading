import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from colorama import init, Fore
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
import nltk
from textblob import TextBlob
from newspaper import Article, ArticleException

init(autoreset=True)

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = set()
    for ent in doc.ents:
        if ent.label_ == "ORG" and len(ent.text.split()) <= 3:
            entities.add(ent.text)
    return entities

def get_headlines(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} Using User-Agent: {headers["User-Agent"]}')

        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} Request successful!')

        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'{Fore.GREEN}[✔]{Fore.WHITE} HTML parsed successfully!')

        headline_elements = soup.find_all('td', class_="news_link-cell")
        print(f'{Fore.BLUE}[✔]{Fore.WHITE} Headlines found successfully!')
        print("------")

        headlines = [headline.text.strip() for headline in headline_elements]
        headline_urls = [headline.find('a')['href'] for headline in headline_elements]

        labels = ['positive', 'negative', 'neutral'] * len(headlines)

        labels = labels[:len(headlines)]

        data = {'headline': headlines, 'url': headline_urls, 'label': labels}
        df = pd.DataFrame(data)

        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)

        return train_data, test_data

    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}[✖] Error: {e}')
        return None, None

def analyse_headlines(train_data, test_data):
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(train_data['headline'])
    X_test = vectorizer.transform(test_data['headline'])

    classifier = LogisticRegression()
    classifier.fit(X_train, train_data['label'])

    analyzer = SentimentIntensityAnalyzer()

    for i, (headline, headline_url) in enumerate(zip(test_data['headline'], test_data['url']), start=1):
        entities = extract_entities(headline)

        sentiment_score = analyzer.polarity_scores(headline)['compound']
        prediction = classifier.predict(vectorizer.transform([headline]))[0]

        if sentiment_score >= 0.1:
            sentiment_label = f'{Fore.GREEN}positive{Fore.RESET}'
            score_color = f'{Fore.GREEN}'
            indicator = f'{Fore.GREEN}[✔]'
        elif sentiment_score <= -0.1:
            sentiment_label = f'{Fore.RED}negative{Fore.RESET}'
            score_color = f'{Fore.RED}'
            indicator = f'{Fore.RED}[✖]'
        else:
            sentiment_label = 'neutral'
            score_color = f'{Fore.RESET}'
            indicator = f'{Fore.RESET}[🔃]'

        prediction_color = f'{Fore.GREEN}' if prediction == 'positive' else f'{Fore.RED}' if prediction == 'negative' else f'{Fore.RESET}'

        entity_display = ', '.join(entities) if entities else 'None'

        print(f"{indicator} {prediction_color}{i}. {Fore.WHITE}{headline}")
        print(f"{Fore.CYAN}[Sentiment] {Fore.WHITE}Prediction: {prediction_color}{prediction} {Fore.RESET}| Score: {score_color}{sentiment_score:.2f} {Fore.RESET}| Sentiment: {sentiment_label} {Fore.RESET}| Entities: {entity_display}{Fore.RESET}")
        print(f"{Fore.YELLOW}[Article URL] {Fore.WHITE}{headline_url}")
        print("----")
        try:
            article = Article(headline_url)
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            # print(f"{Fore.YELLOW}[Article Summary] {Fore.WHITE}{article.summary}")
            blob = TextBlob(text)
            news_sentiment = blob.sentiment.polarity
            if news_sentiment >= 0.1:
                news_sentiment_label = f'{Fore.GREEN}positive{Fore.RESET}'
            elif news_sentiment <= -0.1:
                news_sentiment_label = f'{Fore.RED}negative{Fore.RESET}'
            else:
                news_sentiment_label = f'{Fore.RESET}neutral'
            print(f"{Fore.CYAN}[Article Summary Sentiment] {news_sentiment_label}")

        except ArticleException as article_error:
            print(f'{Fore.RED}[✖] [ARTICLE ERROR]: Could not retrieve article')
            continue  

        print("------------------------------------------------")

if __name__ == "__main__":
    url = 'https://finviz.com/news.ashx'
    train_data, test_data = get_headlines(url)
    if train_data is not None and test_data is not None:
        analyse_headlines(train_data, test_data)
