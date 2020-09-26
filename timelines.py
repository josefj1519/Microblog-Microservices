
from datetime import datetime
from flask import Flask
import pugsql


# Load all of the sql queries into a pugsql module
queries = pugsql.module('queries/')
queries.connect('sqlite:///microblog.db')

app = Flask(__name__)

def getUserTimeline(user):
	tweets = queries.get_user_tweets(username=user)
	return(list(tweets))

def getPublicTimeline():
	tweets = queries.get_all_tweets()
	return(list(tweets))

def getHomeTimeline(user):
	tweets = queries.get_followed_tweets(username=user)
	return(list(tweets))

def postTweet(user, text):
	queries.add_user_tweet(username=user, tweet=text, currentTimestamp=datetime.now())

print(getPublicTimeline())
print(getUserTimeline('williamguy'))

