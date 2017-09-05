import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import json
import os
import joblib
import pandas as pd
import nltk


consumer_key = "g0qkpuI0GCxfmuWKkOF27URNp"
consumer_secret = "DUMJeM2zARcfj3FnYj8XTMuYzZOiYlwSXc3w0yXFGxTJuQP23p"
access_token = "868997754193883136-fuH5kebwOMXV5HZWNEn1uw9i1NXVQHz"
access_secret = "KIXgP1ORmkEC8KOQQu3AgBzclLKkBCpe46SWCIscb57Jr"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
print("TwitterBot Authorized")

user_timeline = api.user_timeline(id="realDonaldTrump", count=10)
print(type(user_timeline), type(user_timeline[0]))

for status in user_timeline:
    print(status.created_at)



