import pytest

from classes.stocks_service import StocksService


@pytest.mark.asyncio(scope="session")
async def test_get_stock_no_amount_returns_zero(true_cache):
    assert await StocksService().get_stock_amount("ALPADL") == 0

@pytest.mark.asyncio(scope="session")
async def test_get_stock_amount_returns_five(true_cache):
    await true_cache.set_value(StocksService().get_record_key("A"), 5)

    assert await StocksService().get_stock_amount("A") == 5

@pytest.mark.asyncio(scope="session")
async def test_add_stock_amount(true_cache):
    assert await StocksService().add_stock("B", 5)

    assert await StocksService().get_stock_amount("B") == 5

@pytest.mark.asyncio(scope="session")
async def test_add_stock_distributed_amount(true_cache):
    assert await StocksService().add_stock("C", 5)
    assert await StocksService().add_stock("C", 5)

    assert await StocksService().get_stock_amount("C") == 10
