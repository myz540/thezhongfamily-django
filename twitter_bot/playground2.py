import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import json
import os
import joblib
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string

def detect_company(text, company_set):
    companies_mentioned = []
    stop_words = stopwords.words() + list(string.punctuation)
    tokens = nltk.word_tokenize(text.lower())
    real_tokens = [token for token in tokens if token not in stop_words]
    print(real_tokens)
    for token in real_tokens:
        for company in company_set:
            company_tokens = nltk.word_tokenize(company.lower())
            if token in company_tokens:
                companies_mentioned.append(company)
                break

    return set(companies_mentioned)


if __name__ == "__main__":
    print(os.getcwd())
    nasdaq = pd.read_csv(r"csv/NASDAQ.csv")
    nyse = pd.read_csv(r"csv/NYSE.csv")

    frames = [nasdaq, nyse]
    df = pd.concat(frames)

    print(type(df))
    #print(df.head())
    #print(df.tail())

    matrix = df.as_matrix()
    company_names = matrix[:,1]

    print(company_names[0], company_names.shape)

    test_text = "Zymeworks and zions bancorporation are terrible!!! " \
                "ZTO Express is garbage too, but 1st Constitution is ok?"

    noteworthy = detect_company(test_text, company_names)

    print(len(noteworthy), noteworthy)


