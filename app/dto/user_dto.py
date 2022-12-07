from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='')

    address=  api.model('Address',{
        'street': fields.String(required=True),
        'city': fields.String(required=True),
        'zipcode': fields.String(required=True),

    })

    user_name =  api.model('UserName', {
        'firstName': fields.String(required=True),
        'lastName': fields.String(required=True),
    })

    user_login_form = api.model('UserLoginForm',{
        'username': fields.String(required=True),
        'password': fields.String(required=True,)
    })

    user_fields = api.model('UserModel', {
        '_id': fields.String(),
        'username': fields.String(),
        'email': fields.String(),
        'photoUrl': fields.String(),
        'name': fields.Nested(user_name),
        'address': fields.Nested(address)
    })

    # user_custom_token = api.model('user_custom_token', {
    #     'name': fields.String(),
    #     'email': fields.String(),
    #     'photoUrl': fields.String(),
    #     'gUserId': fields.String(),
    #     'jobTitle': fields.String(),
    #     'provider': fields.Integer(),
    #     'custom_token': fields.String()
    # })

    # user_usage_status = api.model('user_usage_status', {
    #     # 'contractId': fields.Integer(),
    #     'size': fields.Integer(),
    #     'duration': fields.Integer(),
    # })

    user = api.model('User', {
        'data': fields.Nested(user_fields),
        'statusCode': fields.Integer(required=True, description='response status code'),
        'message': fields.String(required=True, description='response code')
    })

    # user_list = api.model('user_list', {
    #     'data': fields.List(fields.Nested(user_fields)),
    #     'statusCode': fields.Integer(required=True, description='response status code'),
    #     'message': fields.String(required=True, description='response code')
    # })

    # custom_token_response = api.model('custom_token_response', {
    #     'data': fields.Nested(user_custom_token),
    #     'statusCode': fields.Integer(required=True, description='response status code'),
    #     'message': fields.String(required=True, description='response code')
    # })

    # user_usage_status_response = api.model('user_usage_status_response', {
    #     'data': fields.Nested(user_usage_status),
    #     'statusCode': fields.Integer(required=True, description='response status code'),
    #     'message': fields.String(required=True, description='response code')
    # })

    # user_list_usage_status_response = api.model('user_list_usage_status_response', {
    #     'data': fields.List(fields.Nested(user_usage_status)),
    #     'statusCode': fields.Integer(required=True, description='response status code'),
    #     'message': fields.String(required=True, description='response code')
    # })
