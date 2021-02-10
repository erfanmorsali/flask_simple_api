from functools import wraps
from flaskapi.users.services import UserService
from flask_jwt_extended import get_jwt_identity
from flaskapi.posts.services import PostService
from flaskapi.posts.errors import PostErrors
from flaskapi.users.errors import UserErrors

user_service = UserService()
post_service = PostService()
post_errors = PostErrors()
user_errors = UserErrors()

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        identity = get_jwt_identity()
        current_user = user_service.get_user_by_id(identity)
        
        if current_user.is_admin:
            return f(*args,**kwargs)
        else:
            return {"message" : 'permission denied'},403
    
    return decorator

def admin_required_or_post_owner(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        identity = get_jwt_identity()
        current_user = user_service.get_user_by_id(identity)
        post_id = kwargs['id']
        post = post_service.get_post_by_id(post_id)
        if post is None:
            return {"message" : post_errors.post_not_found(post_id)},404
        
        if current_user.is_admin or post.author == current_user:
            return f(*args,**kwargs)
        else:
            return {'message' : "permission denied"},403
            
    return decorator

def admin_or_self_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        identity = get_jwt_identity()
        current_user = user_service.get_user_by_id(identity)
        user = user_service.get_user_by_id(kwargs["id"])
        if user is None:
            return {"message" :  user_errors.user_not_found_by_id(kwargs['id'])},404
        
        if current_user.is_admin or current_user == user:
            return f(*args,**kwargs)
        else:
            return {"message" : "permission denied"},403
    
    return decorator