# CPSC 449 Project 2 Mircoblog Microservices
# by Josef Jankowski and William Timani 
# Josef Jankowski: josefj1519@csu.fullerton.edu
# William Timani: williamtimani@csu.fullerton.edu
# timelines.py contains the timelines microservices.

from datetime import datetime
from flask_api import FlaskAPI, status, exceptions
from flask import request, Blueprint
import pugsql

timelines_api = Blueprint('timelines_api', __name__)
#timelines_api.config.from_envvar('APP_CONFIG')

# Load all of the sql queries into a pugsql module
queries = pugsql.module('queries/')
queries.connect('sqlite:///microblog.db')

# Get a user's timeline. Requires a username as a parameter
# http GET http://127.0.0.1:5000/userTimeline?user=''
# Returns the 25 most recent tweets from the specified user
@timelines_api.route('/userTimeline', methods=['GET'])
def getUserTimeline():
	user = request.args.get('user')

	if not user:
		raise exceptions.ParseError('Error. Parameters incorrect or missing.')

	inDatabase = queries.user_in_database(username=user)
	if not inDatabase:
		return {'error': 'User ' + user + ' does not exist'}, status.HTTP_400_BAD_REQUEST

	tweets = queries.get_user_tweets(username=user)
	return list(tweets), status.HTTP_200_OK

# Get the public timeline.
# http GET http://127.0.0.1:5000/timeline
# Returns the 25 most recent tweets from all users
@timelines_api.route('/timeline', methods=['GET'])
def getPublicTimeline():
	tweets = queries.get_all_tweets()
	return list(tweets), status.HTTP_200_OK

# Get the home timeline for the user
# http GET http://127.0.0.1:5000/home?user=''
# Returns the 25 most recent tweets from all users that the specified user is following
@timelines_api.route('/home', methods=['GET'])
def getHomeTimeline():
	user = request.args.get('user')

	if not user:
		raise exceptions.ParseError('Error. Parameters incorrect or missing.')

	inDatabase = queries.user_in_database(username=user)
	if not inDatabase:
		return {'error': 'User ' + user + ' does not exist'}, status.HTTP_400_BAD_REQUEST

	userFollowees = list(queries.get_followees(username=user))
	followeesList = []
	for users in userFollowees:
		followeesList.append(users.get('followee'))

	tweets = queries.get_followed_tweets(followees=followeesList)

	return list(tweets), status.HTTP_200_OK

# Post a tweet under the specified username
# http POST http://127.0.0.1:5000/tweet/create user='' text=''
# If the user exists, writes the tweet to the database and returns a success statement
@timelines_api.route('/tweet/create', methods=['POST'])
def postTweet():
	if not request.json:
		raise exceptions.ParseError('Error. No request found.')
	if not ('user' and 'text' in request.json):
		raise exceptions.ParseError('Error. Parameters incorrect or missing.')

	user = request.json['user']
	text = request.json['text']

	inDatabase = queries.user_in_database(username=user)
	if not inDatabase:
		return {'error': 'User ' + user + ' does not exist'}, status.HTTP_400_BAD_REQUEST

	queries.add_user_tweet(username=user, tweet=text, currentTimestamp=datetime.now())

	return {'success' : 'Tweet successfully posted.'}, status.HTTP_200_OK
