import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.route('/users/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users)
