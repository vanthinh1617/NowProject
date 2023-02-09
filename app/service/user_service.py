from app.model.db import userCollection
from app.model.model import Users
from app.apis.util.exception import NotFoundDataException
from ..util.helpers import _throw
from bson.objectid import ObjectId

class UserService:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_user_by_id(id):
        try:

            
            user = userCollection.find_one({'_id': ObjectId(id)})
            return user
        except NotFoundDataException as e:
            _throw(e)
    # def authenticate(username: str, password: str):
    #     if(not username or not password):
    #         raise Exception("missing field ")
    #     user = userCollection.find_one({ "username":username }
    #     compare_digest(password, "password")

