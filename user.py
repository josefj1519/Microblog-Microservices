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

#TODO: Add a initdb function.

# Returns a table of users. No params required.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users
@app.route('/users', methods=['GET'])
def allUsers():
    all_users = queries.all_users()
    return list(all_users)

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
    return {'success': 'User account succsefully created.'}

# Requires a username and password query parameters.  
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/authenticate username==<username> hashpass==<hashed_password>
@app.route('/users/authenticate', methods=['GET'])
def authenticateUser():
    user = queries.authenticate_user(username=request.args['username'], hashpass=request.args['hashpass'])
    if not list(user):
        return {'error': 'Invalid username or password' }, status.HTTP_403_FORBIDDEN
    return {'success': 'User account succsefully authenticated.'}

# Requires a username as a query parameter.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/followers username==<username>
@app.route('/users/followers', methods=['GET'])
def allUserFollowers():
    followers = queries.check_users_followers(followee=request.args['username'])
    return list(followers)

# Requires a username as a query parameter.
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/following username==<username>
@app.route('/users/following', methods=['GET'])
def allUserFollowees():
    followees= queries.check_following_users(follower=request.args['username'])
    return list(followees)

# Requires a followee and follower POST parameters 
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/follow followee=<followee> follower=<follower>
@app.route('/users/follow', methods=['POST'])
def addFollower():
    followee = request.json['followee']
    follower = request.json['follower']
    #TODO: Check if user exists before adding.
    try:
        queries.start_following_user(followee=followee, follower=follower)
    except Exception as e:
        return {'error': str(e) }, status.HTTP_409_CONFLICT
    return {'success': 'User ' + follower + ' has started following ' + followee}

# Requires a followee and follower DELETE parameters 
# HTTPie commandline example:
# http http://127.0.0.1:5000/users/unfollow followee==<followee> follower=<follower>
@app.route('/users/unfollow', methods=['DELETE'])
def removeFollower():
    followee = request.json['followee']
    follower = request.json['follower']
    #TODO: Do try catch statement or check if users exist before deleting.
    queries.stop_following(followee=followee, follower=follower)
    return {'success': 'User ' + follower + ' has stopped following ' + followee}
