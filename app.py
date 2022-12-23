#document :
#  
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://www.imaginarycloud.com/blog/flask-python/

from flask_jwt_extended import JWTManager
from app import create_app, blueprint
from app.util.helpers import _throw
from app.service.user_service import UserService
import app.util.jwt
from flask import request,Response

@blueprint.before_request
def hook():
    print(request.base_url)
    # if request.base_url is None
    # if request.cookies.get('lang') is None: 
    #     return{"message": "Missing cookie lang"}, 406
    
app = create_app(__name__)
app.register_blueprint(blueprint)


jwt = JWTManager(app)

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = UserService.get_by_user_name(identity.get('username'))
    return user

if __name__ == '__main__':  
    app.run(debug=True)
  
