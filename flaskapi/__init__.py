from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.db'
app.config["SECRET_KEY"] = '2064e12f6a72f51018f1d907f70e7241346c5d7a8864a8c11c'
app.config['JWT_SECRET_KEY'] = '2064e12f6a72f51018f1d907f70e7241346c5d7a8864a8c11c'

db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


from flaskapi.posts.routes import posts
from flaskapi.users.routes import users

app.register_blueprint(posts)
app.register_blueprint(users)


from .models import User,Post