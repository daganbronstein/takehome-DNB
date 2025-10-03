from async_asgi_testclient import TestClient
import pytest

from api.models.stock import StockModel
from main import app

"""
Effectively integration tests, but rather scrappy ones. Integration tests should be elsewhere, and extensive mocking
should be utilized to strictly unit test the API logic independently.
"""

@pytest.mark.asyncio(scope="session")
async def test_get_stock_default():
    async with TestClient(app) as client:
        response = await client.get("/stock/AAPL")

    assert response.status_code == 200

    content = response.json()

    for lit_field_name, field_info in StockModel.model_fields.items():
        field_name = field_info.serialization_alias or lit_field_name
        assert field_name in content


@pytest.mark.asyncio(scope="session")
async def test_add_stock_amount():
    async with TestClient(app) as client:
        await client.post("/stock/AAPL", json={'amount': 5})
        response = await client.get("/stock/AAPL")

    assert response.status_code == 200

    content = response.json()

    assert content['amount'] == 5


@pytest.mark.asyncio(scope="session")
async def test_set_initial_stock_amount():
    async with TestClient(app) as client:
        for i in range(0, 2):
            await client.post("/stock/MSFT", json={'amount': 5})

        response = await client.get("/stock/MSFT")

    assert response.status_code == 200

    content = response.json()

    assert content['amount'] == 10