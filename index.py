import json
import tweepy
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
        # User's tweet contents
        replyContent = "Hey " + str(tweetInfo['user']['screen_name']) + " thanks for asking!\n\nHere's your account info:\n\n" +\
                       "Verified : " + str(tweetInfo['user']['verified']) + "\n" + \
                       "Number of account likes : " + str(tweetInfo['user']['favourites_count']) + "\n" + \
                       "Number of tweets : " + str(tweetInfo['user']['statuses_count']) + "\n"

        # Like the tweet
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                print("Error on fav")

        # Retweet the tweet and send message
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                # Reply to the tweet
                api.update_status(status=replyContent, in_reply_to_status_id=tweetInfo['id'],
                                  auto_populate_reply_metadata=True)
            except Exception as e:
                print("Error or tweet has already been retweeted")
    def on_error(self, status):
        print("Error detected: " + str(status))


# Authenticate to Twitter
auth = tweepy.OAuthHandler(APIKEY,APISECRET)
auth.set_access_token(OAUTHTOKEN,OAUTHTOKENSECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["What's my profile status?","Whats my profile status?"], languages=["en"],is_async=True)