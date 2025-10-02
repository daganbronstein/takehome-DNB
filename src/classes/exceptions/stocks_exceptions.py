from classes.app_exception import AppException


class StocksGenericException(AppException):
    code = "2000"

class StocksBadTotalException(StocksGenericException):
    code = "2001"