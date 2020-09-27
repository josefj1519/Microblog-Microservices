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

#Returns a table of users. No params required.
@app.route('/users', methods=['GET'])
def allUsers():
    all_users = queries.all_users()
    return list(all_users)

#Creates a new user tuple.
#Requires a username, email, and password POST parameters.  
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

#Requires a username and password query parameters.  
@app.route('/users/authenticate', methods=['GET'])
def authenticateUser():
    user = queries.authenticate_user(username=request.args['username'], hashpass=request.args['hashpass'])
    if not list(user):
        return {'error': 'Invalid username or password' }, status.HTTP_403_FORBIDDEN
    return {'success': 'User account succsefully authenticated.'}