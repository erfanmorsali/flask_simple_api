from .interfaces import UserInterface
from flaskapi.models import User
from flaskapi import db,bcrypt
import datetime
from flask_jwt_extended import create_access_token

class UserService(UserInterface):
    
    
    def get_all_users(self):    
        return User.query.all()

    def get_user_by_id(self,id):
        return User.query.get(id)

    def get_user_by_email(self,email):
        return User.query.filter_by(email=email).first()

    def update_user(self,user_id,dictionary):
        user = User.query.filter_by(id=user_id).update(dictionary)
        db.session.commit()

    def register_user(self,username,email,password):
        hashed_password = self.generate_hash_password(password)
        new_user = User(username=username,email=email,password=hashed_password)
        self.add_user_to_database(new_user)
    
    def generate_hash_password(self,password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_user_password(self,user,password):
        return bcrypt.check_password_hash(user.password, password)


    def add_user_to_database(self,user):
        db.session.add(user)
        db.session.commit()

    def delete_user(self,user):
        db.session.delete(user)
        db.session.commit()

    def generate_json_web_token(self,id):
        token_expire_time = datetime.timedelta(days=1)
        return create_access_token(id, expires_delta=token_expire_time)