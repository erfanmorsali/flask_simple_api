from marshmallow import Schema, fields , validate 
from flaskapi.users.serializers import UserSerializer

class PostSerializer(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    author = fields.Nested(UserSerializer())


class CreatePostSerializer(Schema):
    title = fields.Str(required=True,validate=validate.Length(min=8,max=30))
    content = fields.Str(required=True)
    author = fields.Int(required=True)


class UpdatePostSerializer(Schema):
    title = fields.Str(validate=validate.Length(min=8,max=30)) 
    content = fields.Str()
    user_id = fields.Int()