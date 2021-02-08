from .interfaces import PostInterface
from flaskapi.models import Post
from flaskapi import db
from flaskapi.users.services import UserService

user_service = UserService()


class PostService(PostInterface):

    def get_post_by_id(self,id):
        post = Post.query.get(id)
        return post

    def get_all_posts(self):
        return Post.query.all()

    def add_post_to_database(self,post):
        db.session.add(post)
        db.session.commit()

    def create_post(self,title,content,author_id):
        author = self.check_author_exists(author_id)
        if author is None:
            return None
        p = Post(title=title,content=content,author=author)
        self.add_post_to_database(p)
        return p

    def delete_post(self,post):
        db.session.delete(post)
        db.session.commit()


    def check_author_exists(self,id):
        user = user_service.get_user_by_id(id)
        return user

    def update_post(self,post_id,dictionary):
        author = dictionary.get("user_id")
        if author is not None:
            author = user_service.get_user_by_id(author)
            if author is None:
                return None
        p = Post.query.filter_by(id=post_id).update(dictionary)
        db.session.commit()
        return p