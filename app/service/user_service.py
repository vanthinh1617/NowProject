from app.model.db import userCollection
from app.model.model import Users
from ..util.helpers import _throw
from app.util.jwt import create_token
import bcrypt
class UserService:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def authenticate(username: str, password: str):
        if(not username or not password):
            _throw(Exception('missing field '))
        user = userCollection.find_one({ "username":username })
        user = Users(**user)
     
        if user is None or UserService.check_password(password, user.password) == False:
            _throw(Exception('please check your username or password'))

        access_token = create_token(dict(username= user.username, email=user.email))
        return {"access_token": access_token}

    @staticmethod
    def register(data):
        try:
            user = Users(**data)
            user.password = UserService.get_hashed_password(user.password)
            userCollection.insert_one(user.to_bson())
            access_token = create_token(dict(username= user.username, email=user.email))

            return {"message":"Register success" ,"access_token": access_token}
        except Exception as e:
            _throw(e)

    @staticmethod
    def getLists(page:int = 1, pageSize: int= 30):
        page = int(page)
        pageSize = int(pageSize)
        userList =  userCollection.find().skip((page - 1) * pageSize).limit(pageSize)
        return   list(userList)