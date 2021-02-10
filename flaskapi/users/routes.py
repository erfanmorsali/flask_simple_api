from .serializers import UserSerializer,UpdateUserSerializer,CreateUserSerializer,LoginSerializer
from flask import Blueprint , jsonify , request
from flask_restful import Resource
from .services import UserService
from flaskapi import api
from .errors import UserErrors
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from .decorators import admin_required

users = Blueprint("users",__name__)
user_service = UserService()
user_errors = UserErrors()


class AllUsersView(Resource):
    @jwt_required
    @admin_required
    def get(self):
        users = user_service.get_all_users()
        serializer = UserSerializer(many=True).dump(users)
        return jsonify(serializer)

class UserDetailView(Resource):
    def get(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)} , 404
        serializer = UserSerializer().dump(user)
        return jsonify(serializer)
    
    def put(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)} ,404
        try:
            serializer = UpdateUserSerializer().load(request.json)
            user_service.update_user(id,serializer)
            return {"message" : "user successfully updated"} , 202
        except ValidationError as err:
            return {"message" : err.messages} , 400


    def delete(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)} , 404
        user_service.delete_user(user)
        return {"message" : "user successfully deleted"} , 200


class CreateUserView(Resource):
    def post(self):
        try:
            serializer = CreateUserSerializer().load(request.json)
            user_service.register_user(serializer['username'],serializer['email'],serializer['password'])
            return {"message" : "user successfully created"} , 201
        except ValidationError as err:
            return {"message" : err.messages} , 400


class Login(Resource):
    def post(self):
        try:
            serializer = LoginSerializer().load(request.json)
            user = user_service.get_user_by_email(serializer["email"])
            if user and user_service.check_user_password(user,serializer["password"]):
                token = user_service.generate_json_web_token(user.id)
                return {'access-token' : token},200
            else:
                return {"message" : "user not found"}
        except ValidationError as err:
            return {"message" : err.messages}

api.add_resource(AllUsersView,"/all_users")
api.add_resource(UserDetailView,"/user_by_id/<int:id>")
api.add_resource(CreateUserView,"/create_user")
api.add_resource(Login,"/login")