from app.model.db import userCollection
from app.model.model import Users


class UserService:
    def __init__(self) -> None:
        pass

    # def authenticate(username: str, password: str):
    #     if(not username or not password):
    #         raise Exception("missing field ")
    #     user = userCollection.find_one({ "username":username }
    #     compare_digest(password, "password")

