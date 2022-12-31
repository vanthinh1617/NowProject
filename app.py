#document :
#  
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://www.imaginarycloud.com/blog/flask-python/

from flask_jwt_extended import JWTManager
from app import create_app, blueprint
from app.util.helpers import _throw
from app.service.user_service import UserService
from app.util.i18n import run as translate, beforeRequest as i18nBeforeRequest

import app.util.jwt
from flask import request,Response


app = create_app(__name__)
jwt = JWTManager(app)
app.register_blueprint(blueprint)

@app.before_request
def before_request():
    i18nBeforeRequest() 

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = UserService.get_by_user_name(identity.get('username'))
    return user 
translate(__file__+"/translate/lang")
if __name__ == '__main__':  
    app.run(debug=True)
  
