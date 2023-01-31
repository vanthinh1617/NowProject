from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import current_user
import datetime

def create_token(user):
    return  create_access_token(identity=user)

def get_jwt_identity():
    return get_jwt_identity()

# Hàm gọi đến user_lookup_loader để lấy dữ liệu
def get_current_user():
    return current_user

def get_exprive_time():
    return datetime.timedelta(days= 1)