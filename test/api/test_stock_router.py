from fastapi.testclient import TestClient

from api.models.stock import StockModel
from main import app

client = TestClient(app)

"""
Effectively integration tests, but rather scrappy ones. Integration tests should be elsewhere, and extensive mocking
should be utilized to strictly unit test the API logic independently.
"""

def test_get_stock_default():
    response = client.get("/stock/AAPL")

    assert response.status_code == 200

    content = response.json()

    for lit_field_name, field_info in StockModel.model_fields.items():
        field_name = field_info.serialization_alias or lit_field_name
        assert field_name in content


def test_add_stock_amount(true_cache):
    client.post("/stock/AAPL", json={'amount': 5})

    response = client.get("/stock/AAPL")

    assert response.status_code == 200

    content = response.json()

    assert content['amount'] == 5


def test_set_initial_stock_amount(true_cache):
    for i in range(0, 2):
        client.post("/stock/MSFT", json={'amount': 5})

    response = client.get("/stock/MSFT")

    assert response.status_code == 200

    content = response.json()

    assert content['amount'] == 10