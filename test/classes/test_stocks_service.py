from classes.stocks_service import StocksService


def test_get_stock_no_amount_returns_zero(true_cache):
    assert StocksService().get_stock_amount("ALPADL") == 0

def test_get_stock_amount_returns_five(true_cache):
    true_cache.set_value(StocksService().get_record_key("A"), 5)

    assert StocksService().get_stock_amount("A") == 5

def test_add_stock_amount(true_cache):
    assert StocksService().add_stock("B", 5)

    assert StocksService().get_stock_amount("B") == 5

def test_add_stock_distributed_amount(true_cache):
    assert StocksService().add_stock("C", 5)
    assert StocksService().add_stock("C", 5)

    assert StocksService().get_stock_amount("C") == 10
