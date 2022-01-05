import json
import tweepy
from time import *
from os import environ

APIKEY = environ['Consumer_Key']
APISECRET = environ['Consumer_Secret']
OAUTHTOKEN = environ['Access_Key']
OAUTHTOKENSECRET = environ['Access_Secret']

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        tweetInfo = json.loads(json.dumps(tweet._json))

        # Guard clause for retweets of original tweet
        if 'retweeted_status' in tweetInfo or 'quoted_status_permalink' in tweetInfo:
            return
        
        # Guard clause for possibly sensitive tweets
        if 'possibly_sensitive' in tweetInfo and tweetInfo['possibly_sensitive']:
            return
        
        # Guard clause for tweets with more than 5 hashtags
        if len(tweetInfo['entities']['hashtags']) > 5:
            print("Tweet with more than 5 hashtags detected. Ignoring...")
            return

        # Guard clause for extended tweets with more than 5 hashtags
        if 'extended_tweet' in tweetInfo and len(tweetInfo['extended_tweet']['entities']['hashtags']) > 5:
            print("Extended tweet with more than 5 hashtags detected. Ignoring...")
            return

        # Like the tweet
        if not tweet.favorited:
            try:
                tweet.favorite()
                sleep(12)
            except Exception as e:
                print("Error liking tweet because: " + str(e))

    def on_error(self, status):
        if status == 420:
            print("Error detected: " + str(status) + "\nClosing and reconnecting the Stream...")
            # Wait 15 min before reconnecting
            sleep(900)
            return False
        else:
            print("Error detected: " + str(status))


# Authenticate to Twitter
auth = tweepy.OAuthHandler(APIKEY,APISECRET)
auth.set_access_token(OAUTHTOKEN,OAUTHTOKENSECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["#crypto","#nft","#web3"],is_async=True)
