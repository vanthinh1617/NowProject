from flask import Flask, Blueprint
from flask_restx import Api

from app.model.db import initialize_db
from .controller.UserController import api as user_namespace
from app.util.exception import DuplicateDataException
from app.util.helpers import _throw
import datetime
blueprint = Blueprint('api',__name__, url_prefix="/api")

@blueprint.app_errorhandler(DuplicateDataException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
    _throw(error)

api = Api(blueprint)
api.add_namespace(user_namespace,path='/user')


def create_app(name):
    app = Flask(name)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    app.config["JWT_SECRET_KEY"] = "now-project-key"  # Change this "super secret" with something else!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=1)
    initialize_db(app)
    return app