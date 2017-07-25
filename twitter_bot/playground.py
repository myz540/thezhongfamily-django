import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import json
import os


class TwitterBot(StreamListener):
    """
    Consumer Key (API Key)	g0qkpuI0GCxfmuWKkOF27URNp
    Consumer Secret (API Secret)	DUMJeM2zARcfj3FnYj8XTMuYzZOiYlwSXc3w0yXFGxTJuQP23p
    """
    def __init__(self):
        self.consumer_key = "g0qkpuI0GCxfmuWKkOF27URNp"
        self.consumer_secret = "DUMJeM2zARcfj3FnYj8XTMuYzZOiYlwSXc3w0yXFGxTJuQP23p"
        self.access_token = "868997754193883136-fuH5kebwOMXV5HZWNEn1uw9i1NXVQHz"
        self.access_secret = "KIXgP1ORmkEC8KOQQu3AgBzclLKkBCpe46SWCIscb57Jr"
        self.api = None
        super().__init__()
        print("TwitterBot initialized")

    def auth(self):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        self.api = tweepy.API(auth)
        print("TwitterBot Authorized")

    def process_or_store(self, tweet):
        pass

if __name__ == "__main__":
    bot = TwitterBot()
    bot.auth()

    print("HI")