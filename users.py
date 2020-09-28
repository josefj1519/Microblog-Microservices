# CPSC 449 Project 2 Mircoblog Microservices
# by Josef Jankowski and William Timani 
# Josef Jankowski: josefj1519@csu.fullerton.edu
# William Timani: williamtimani@csu.fullerton.edu
# users.py contains the users microservice and flask init.
 
import click
import flask_api
import pugsql
from flask import request
from flask_api import status, exceptions
from werkzeug.security import generate_password_hash, check_password_hash
from timelines import timelines_api

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
app.register_blueprint(timelines_api)

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

# Initilize the databse with the queries and inserts from schema.sql.
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries.engine.raw_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Returns a table of users. No params required.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users
@app.route('/users', methods=['GET'])
def allUsers():
    all_users = queries.all_users()
    return list(all_users), status.HTTP_200_OK

# Creates a new user tuple.
# Requires a username, email, and password POST parameters.  
# HTTPie commandline example:
# http POST http://127.0.0.1:5000/users/create username='' email='' password=''
@app.route('/users/create', methods=['POST'])
def createUser():
    if not request.json:
        raise exceptions.ParseError('Error. No request found.')
    if not ('username' and 'email'  and 'password' in request.json):
        raise exceptions.ParseError('Error. Parameters incorrect or missing.')
    username = request.json['username']
    email = request.json['email']
    hashpass = generate_password_hash(request.json['password'], method='pbkdf2:sha256', salt_length=8)
    try:
        queries.create_user(username=username, email=email, hashpass=hashpass)
    except Exception as e:
        return {'error': str(e) }, status.HTTP_409_CONFLICT
    return {'success': 'User account succsefully created.'}, status.HTTP_200_OK

# Requires a username and password query parameters.  
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/authenticate username==<username> hashpass==<hashed_password>
@app.route('/users/authenticate', methods=['GET'])
def authenticateUser():
    user = queries.authenticate_user(username=request.args['username'], hashpass=request.args['hashpass'])
    if not list(user):
        return {'error': 'Invalid username or password' }, status.HTTP_403_FORBIDDEN
    return {'success': 'User account succsefully authenticated.'}, status.HTTP_200_OK

# Requires a username as a query parameter.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/followers username==<username>
@app.route('/users/followers', methods=['GET'])
def allUserFollowers():
    followers = queries.check_users_followers(followee=request.args['username'])
    return list(followers), status.HTTP_200_OK

# Requires a username as a query parameter.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/following username==<username>
@app.route('/users/following', methods=['GET'])
def allUserFollowees():
    followees = queries.check_following_users(follower=request.args['username'])
    return list(followees), status.HTTP_200_OK

# Requires a followee and follower POST parameters 
# HTTPie commandline example:
# http POST http://127.0.0.1:5000/users/follow followee=<followee> follower=<follower>
@app.route('/users/follow', methods=['POST'])
def addFollower():
    followee = request.json['followee']
    follower = request.json['follower']
    if not checkUser(followee) or not checkUser(follower):
        return {'error': 'User does not exist.' }, status.HTTP_400_BAD_REQUEST
    try:
        queries.start_following_user(followee=followee, follower=follower)
    except Exception as e:
        return {'error': str(e) }, status.HTTP_409_CONFLICT
    return {'success': 'User ' + follower + ' has started following ' + followee}, status.HTTP_200_OK

# Requires a followee and follower DELETE parameters 
# HTTPie commandline example:
# http DELETE http://127.0.0.1:5000/users/unfollow followee==<followee> follower=<follower>
@app.route('/users/unfollow', methods=['DELETE'])
def removeFollower():
    followee = request.json['followee']
    follower = request.json['follower']
    if not checkIfFollowing(followee, follower):
         return {'error': 'User does not exist or is not following the followee.' }, status.HTTP_400_BAD_REQUEST
    queries.stop_following(followee=followee, follower=follower)
    return {'success': 'User ' + follower + ' has stopped following ' + followee}, status.HTTP_200_OK

# Check if the username is in the database.  
def checkUser(username):
    check_for_user = queries.check_for_user(username=username)
    return check_for_user

# Checks if the follower is following the followee
def checkIfFollowing(followee, follower):
    check_if_following = queries.check_if_following(followee=followee, follower=follower)
    return check_if_following
