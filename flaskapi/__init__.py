from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'

db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)

from flaskapi.posts.routes import posts
from flaskapi.users.routes import users

app.register_blueprint(posts)
app.register_blueprint(users)


from .models import User,Post