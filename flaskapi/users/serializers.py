from marshmallow import Schema, fields , validate 



class UserSerializer(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    posts = fields.List(fields.Nested("PostSerializer",exclude=("author",)))


class UpdateUserSerializer(Schema):
    username = fields.Str(validate=validate.Length(min=5,max=30))
    email = fields.Email(validate=validate.Length(min=8,max=50))


class CreateUserSerializer(Schema):
    username = fields.Str(required=True,validate=validate.Length(min=5,max=30))
    email = fields.Email(required=True,validate=validate.Length(min=8,max=50))
    password = fields.Str(required=True,validate=validate.Length(min=6,max=50))


class LoginSerializer(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
