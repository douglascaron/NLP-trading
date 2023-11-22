from nltk.sentiment import SentimentIntensityAnalyzer

while True: 
    data = input("News: ")

    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(data)['compound']
    print(sentiment_score)