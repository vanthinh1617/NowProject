
from flask_restx import abort
import json
import bleach
from app.util.const import Const

def _throw(exception):
    _error_abort(str(exception))


def _error_abort(mess):
    """Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'statusCode': 500,
        'message': mess
    }
    abort(500, **error)

def _success(message, data):
    """Abstraction over restplus `abort`.
    Returns success with the status code and message.
    """
    json_string = json.dumps(
        data, indent=4, sort_keys=True, ensure_ascii=False, default=str)
    json_string_clean = bleach.clean(json_string)
    response = {
        'statusCode': 200,
        # 'message': f"{HTTP_STATUS_CODES[200]} : {_response_message(message[0][3])}",
        'data': json.loads(json_string_clean)
    }
    return response, Const.ResponseCode.SUCCESS


def _response_message(func_name):
    func_name = func_name.replace(
        Const.SpecialChar.UNDERSCORE, Const.SpecialChar.SPACE)
    return Const.ResponseMessage.SUCCESS + func_name