from flask import Blueprint , jsonify , request
from flaskapi.models import Post
from .services import PostService
from .serializers import PostSerializer,CreatePostSerializer,UpdatePostSerializer
from flask_restful import Resource
from flaskapi import api
from marshmallow import ValidationError
from .errors import PostErrors
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskapi.decorators import admin_required,admin_required_or_post_owner
from flaskapi.users.services import UserService

posts = Blueprint("posts",__name__)
post_service = PostService()
post_errors = PostErrors()
user_service = UserService()

class AllPostsView(Resource):
    @jwt_required
    @admin_required
    def get(self):
        query = post_service.get_all_posts()
        serializer = PostSerializer(many=True).dump(query)
        return jsonify(serializer)

class PostDetailView(Resource):
    
    @jwt_required
    @admin_required_or_post_owner
    def get(self,id):
        query = post_service.get_post_by_id(id)
        serializer = PostSerializer().dump(query)
        return jsonify(serializer)
    
    
    @jwt_required
    @admin_required_or_post_owner
    def delete(self,id):
        post = post_service.get_post_by_id(id)
        if post is None:
            return {"message" : post_errors.post_not_found(id)},404
        post_service.delete_post(post)
        return {"message" : "post successfully deleted"},202

    
    @jwt_required
    @admin_required_or_post_owner
    def put(self,id):
        try:
            post = post_service.get_post_by_id(id)
            serializer = UpdatePostSerializer().load(request.json)
            updated_post = post_service.update_post(post.id,serializer)
            result = PostSerializer().dump(post)
            return jsonify(result)
        except ValidationError as err:
            return {"message" : err.messages},400

class CreatePostView(Resource):
    @jwt_required
    def post(self):
        try:
            user = user_service.get_user_by_id(get_jwt_identity())
            serializer = CreatePostSerializer().load(request.json)
            new_post = post_service.create_post(serializer["title"],serializer["content"],user)
            return {"message" : f"post with id {new_post.id} successfully created"},201
        except ValidationError as err:
            return {"message" : err.messages},400

api.add_resource(AllPostsView,"/all_posts")
api.add_resource(PostDetailView,"/post_by_id/<int:id>")
api.add_resource(CreatePostView,"/create_post")


