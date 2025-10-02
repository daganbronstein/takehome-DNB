import threading

from classes.cache import CacheService
from classes.exceptions.stocks_exceptions import StocksBadTotalException
from enums.cache_keys import CacheKeys


class StocksService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super(StocksService, cls).__new__(cls)
        return cls._instance

    def get_stock_amount(self, stock_symbol: str) -> int:
        record_key: str = self.get_record_key(stock_symbol)
        stock_amount: int = int(CacheService().get_value(record_key) or 0)

        return stock_amount

    def add_stock(self, stock_symbol: str, added_amount: int) -> int:
        # Acquire a db-side lock. This will guarantee the atomicity of our operation,
        #   even across multiple uvicorn processes. It is possible that a pipeline will also be better, but
        #   without plenty of boilerplate, it will couple redis with the stocks service too much.
        with CacheService().lock(stock_symbol) as lock:
            current_amount: int = self.get_stock_amount(stock_symbol)
            new_amount: int = current_amount + added_amount

            if new_amount < 0:
                raise StocksBadTotalException(message="New amount is less than 0")

            record_key: str = self.get_record_key(stock_symbol)
            CacheService().set_value(record_key, new_amount)

        return new_amount

    @staticmethod
    def get_record_key(stock_symbol: str) -> str:
        return f'{CacheKeys.USER_VALUE}:{stock_symbol}'