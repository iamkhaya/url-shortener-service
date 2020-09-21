# pylint: disable=super-init-not-called
class APIException(Exception):
    def __init__(self, message=None, status_code=500):
        self.status_code = status_code
        self.message = message if message else "Service Error"

    def get_status_code(self):
        return self.status_code

    def to_dict(self):
        dto = {"status_code": self.status_code, "message": self.message}
        return dto


class ValidationException(APIException):
    def __init__(self, message=None):
        self.status_code = 400
        self.message = message if message else "Invalid value"


class ItemNotFoundException(APIException):
    def __init__(self, message=None):
        self.status_code = 404
        self.message = message if message else "Item not found"


class MethodNotAllowedException(APIException):
    def __init__(self, message=None):
        self.status_code = 405
        self.message = message if message else "Method Not Allowed"


class BadGatewayException(APIException):
    def __init__(self, message=None):
        self.status_code = 502
        self.message = message if message else "Bad Gateway"


class GatewayTimeoutException(APIException):
    def __init__(self, message=None):
        self.status_code = 504
        self.message = message if message else "Gateway Timeout"


class BadAuditConfigException(APIException):
    def __init__(self, message=None):
        self.message = message if message else "Bad Audit Configuration"


class TransitionError(APIException):
    def __init__(self, message=None):
        self.message = message if message else "Failed state transition"
