from .interfaces import PostInterface
from flaskapi.models import Post
from flaskapi import db


class PostService(PostInterface):

    def get_post_by_id(self,id):
        post = Post.query.get(id)
        return post

    def get_all_posts(self):
        return Post.query.all()

    def add_post_to_database(self,post):
        db.session.add(post)
        db.session.commit()

    def create_post(self,title,content,author):
        p = Post(title=title,content=content,author=author)
        self.add_post_to_database(p)
        return p

    def delete_post(self,post):
        db.session.delete(post)
        db.session.commit()

    def update_post(self,post_id,dictionary):
        p = Post.query.filter_by(id=post_id).update(dictionary)
        db.session.commit()
        return p