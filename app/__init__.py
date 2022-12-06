from flask import Flask, Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.model.db import initialize_db
from .controller.UserController import api as user_namespace
blueprint = Blueprint('api',__name__, url_prefix="/api")
api = Api(blueprint)
api.add_namespace(user_namespace,path='/user')

def create_app(name):
    app = Flask(name)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    app.config["JWT_SECRET_KEY"] = "now-project-key"  # Change this "super secret" with something else!
    JWTManager(app)

    initialize_db(app)
    return app