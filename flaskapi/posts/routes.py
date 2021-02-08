from flask import Blueprint , jsonify , request
from flaskapi.models import Post
from .services import PostService
from .serializers import PostSerializer,CreatePostSerializer,UpdatePostSerializer
from flask_restful import Resource
from flaskapi import api
from marshmallow import ValidationError
from .errors import PostErrors

posts = Blueprint("posts",__name__)


post_service = PostService()
post_errors = PostErrors()


class AllPostsView(Resource):
    def get(self):
        query = post_service.get_all_posts()
        serializer = PostSerializer(many=True).dump(query)
        return jsonify(serializer)

class PostDetailView(Resource):
    def get(self,id):
        query = post_service.get_post_by_id(id)
        if query is None:
            return {"message" : post_errors.post_not_found(id)}
        serializer = PostSerializer().dump(query)
        return jsonify(serializer)


    def delete(self,id):
        post = post_service.get_post_by_id(id)
        if post is None:
            return {"message" : post_errors.post_not_found(id)}
        post_service.delete_post(post)
        return {"message" : "post successfully deleted"}


    def put(self,id):
        post = post_service.get_post_by_id(id)
        if post is None:
            return {"message" : post_errors.post_not_found(id)}
        try:
            serializer = UpdatePostSerializer().load(request.json)
            updated_post = post_service.update_post(post.id,serializer)
            if updated_post is None:
                return {"message" : post_errors.author_not_found(serializer["user_id"])}
            else:
                result = PostSerializer().dump(post)
                return jsonify(result)
        except ValidationError as err:
            return {"message" : err.messages}

class CreatePostView(Resource):
    def post(self):
        try:
            serializer = CreatePostSerializer().load(request.json)
            new_post = post_service.create_post(serializer["title"],serializer["content"],serializer["author"])
            if new_post is not None:
                return {"message" : f"post with id {new_post.id} successfully created"}
            else:
                return {"message" : post_errors.author_not_found(serializer["author"])}
        except ValidationError as err:
            return {"message" : err.messages}

api.add_resource(AllPostsView,"/all_posts")
api.add_resource(PostDetailView,"/post_by_id/<int:id>")
api.add_resource(CreatePostView,"/create_post")


