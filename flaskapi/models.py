from flaskapi import db


class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    is_admin = db.Column(db.Boolean,default=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship("Post",backref="author",cascade="all, delete-orphan",lazy=True)

    def __repr__(self):
        return f"User({self.id} {self.username})"



class Post(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey("user.id"),nullable=False)   

    def __repr__(self):
        return f'Post({self.id} {self.title})'

