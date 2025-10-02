from classes.app_exception import AppException


class PolygonGenericException(AppException):
    error_code: str = "1000"

class PolygonConnectionError(PolygonGenericException):
    error_code: str = "1001"

class PolygonJSONError(PolygonGenericException):
    error_code: str = "1002"