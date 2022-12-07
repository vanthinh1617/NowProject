from app.util.const import Const
# from ..util.logging import logger


class DuplicateDataException(Exception):
    status_code = 409

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class NotFoundDataException(Exception):
    status_code = 412

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)
        pass


class LackArgumentException(Exception):
    status_code = 412

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)
        pass


class UnauthorizedException(Exception):
    status_code = 401

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)
        pass


class NotPermissionException(Exception):
    status_code = 413

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)
        pass

class NotPermissionException(Exception):
    status_code = 413

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        # logger.error(Const.LOG_LEVEL.EXCEPTION, exc_info=True)
        pass
