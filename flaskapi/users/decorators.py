from functools import wraps
from .services import UserService
from flask_jwt_extended import get_jwt_identity

user_service = UserService()

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