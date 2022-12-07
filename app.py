#document :
#  
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
# https://www.imaginarycloud.com/blog/flask-python/

from flask_jwt_extended import JWTManager
from app import create_app, blueprint
from app.util.helpers import _throw

app = create_app(__name__)
app.register_blueprint(blueprint)

jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_loader_callback(s):
   _throw(s)


if __name__ == '__main__':  
    app.run(debug=True)
  
