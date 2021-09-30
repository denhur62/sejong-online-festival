"""
API Main Decorator
"""
import json
from functools import wraps
from time import time
from flask import current_app, g, Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.api import forbidden
from model.mongodb import User


def timer(func):
    """API Timer"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_time = time()
        result = func(*args, **kwargs)
        g.process_time = time() - process_time

        if current_app.config['DEBUG']:
            if isinstance(result, Response):
                data = json.loads(result.get_data())
                data['process_time'] = g.process_time
                result.set_data(json.dumps(data))
            elif isinstance(result, tuple):
                result[0]['process_time'] = g.process_time
            else:
                result['process_time'] = g.process_time
        return result
    return wrapper


def login_required(role: str):
    def real_decorator(func):
        @wraps(func)
        def wrappper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user_model = User(g.db)
            if not identity or not user_model.get_identity(identity['user_id']):
                return {"msg": "Bad access token."}, 401
            if 'admin' not in identity['roles'] and role not in identity['roles']:
                return forbidden("Permission denied.")
            g.user_id = identity['user_id']
            g.roles = identity['roles']
            return func(*args, **kwargs)
        return wrappper
    return real_decorator