
from datetime import datetime
from flask_api import FlaskAPI
from flask import request, Blueprint
import pugsql

timelines_api = Blueprint('timelines_api', __name__)
#timelines_api.config.from_envvar('APP_CONFIG')

# Load all of the sql queries into a pugsql module
queries = pugsql.module('queries/')
queries.connect('sqlite:///microblog.db')

@timelines_api.route('/userTimeline', methods=['GET'])
def getUserTimeline():
	user = request.args.get('user')
	tweets = queries.get_user_tweets(username=user)
	return list(tweets)

@timelines_api.route('/timeline', methods=['GET'])
def getPublicTimeline():
	tweets = queries.get_all_tweets()
	return list(tweets)

@timelines_api.route('/home', methods=['GET'])
def getHomeTimeline():
	user = request.args.get('user')

	userFollowees = list(queries.get_followees(username=user))
	followeesList = []
	for users in userFollowees:
		followeesList.append(users.get('followee'))

	tweets = queries.get_followed_tweets(followees=followeesList)

	return list(tweets)

@timelines_api.route('/tweet/create', methods=['PUT'])
def postTweet(user, text):
	queries.add_user_tweet(username=user, tweet=text, currentTimestamp=datetime.now())
