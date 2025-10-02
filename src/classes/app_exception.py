import logging

logger = logging.getLogger(__name__)

class AppException(Exception):
    # No explicit subtyping. Can have key "data" or "exception", unknown type value. Better solution needed
    debug: dict
    message: str
    error_code: str = "0000"

    def __init__(self, message: str, **kwargs):
        super().__init__(message)
        self.message = message
        self.debug = kwargs
