from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt import JWT
import sqlite3
from flask_cors import CORS

from security import authenticate, identity
from user import UserRegister
from article import Article, ArticleList
from event import Event, EventList

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'momo'
api = Api(app)


jwt = JWT(app, authenticate, identity)

api.add_resource(Article, '/article/<string:name>')
api.add_resource(ArticleList, '/articles')
api.add_resource(UserRegister, '/register')
api.add_resource(Event, '/event/<string:name>')
api.add_resource(EventList, '/events')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True


