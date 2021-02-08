from .serializers import UserSerializer,UpdateUserSerializer,CreateUserSerializer
from flask import Blueprint , jsonify , request
from flask_restful import Resource
from .services import UserService
from flaskapi import api
from .errors import UserErrors
from marshmallow import ValidationError


users = Blueprint("users",__name__)
user_service = UserService()
user_errors = UserErrors()


class AllUsersView(Resource):
    def get(self):
        users = user_service.get_all_users()
        serializer = UserSerializer(many=True).dump(users)
        return jsonify(serializer)


class UserDetailView(Resource):
    def get(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)}
        serializer = UserSerializer().dump(user)
        return jsonify(serializer)
    
    def put(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)}
        try:
            serializer = UpdateUserSerializer().load(request.json)
            user_service.update_user(id,serializer)
            return {"message" : "user successfully updated"}
        except ValidationError as err:
            return {"message" : err.messages}


    def delete(self,id):
        user = user_service.get_user_by_id(id)
        if user is None:
            return {"message" : user_errors.user_not_found_by_id(id)}
        user_service.delete_user(user)
        return {"message" : "user successfully deleted"}


class CreateUserView(Resource):
    def post(self):
        try:
            serializer = CreateUserSerializer().load(request.json)
            user_service.register_user(serializer['username'],serializer['email'],serializer['password'])
            return {"message" : "user successfully created"}
        except ValidationError as err:
            return {"message" : err.messages}




api.add_resource(AllUsersView,"/all_users")
api.add_resource(UserDetailView,"/user_by_id/<int:id>")
api.add_resource(CreateUserView,"/create_user")