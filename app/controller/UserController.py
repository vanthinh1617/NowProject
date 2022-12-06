from flask_restx import Resource
from flask import request
from ..dto.user_dto  import UserDto
from app.model.model import User
api = UserDto.api
_resp = UserDto.user_fields

@api.route('/getUsers')
class UserList(Resource):
    def get(self):
        return   request.args

    @api.marshal_with(_resp, code=201)
    # @api.expect(_resp)
    def post(self):
        return  User(**api.payload).to_json()
        # return {"data": api.payload, "code": 200}
       
        
@api.route('/')
class HomePage(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/login')
class Login(Resource):

    @api.expect(UserDto.user_login_form)
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        # if username != "test" or password != "test":
        #     return jsonify({"msg": "Bad username or password"}), 401
        

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)