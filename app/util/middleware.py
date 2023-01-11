from functools import wraps
from flask import  request, Response

def cookie_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.cookies.get('lang') is None:
            return {'message': 'required cookie "lang"'}
        return f(*args, **kwargs)
    return decorated_function