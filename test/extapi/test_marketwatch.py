import pydantic
import pytest

from extapi.marketwatch import marketwatch_get_performance
from models.marketwatch_record import MarketwatchRecord


@pytest.fixture(scope='session')
async def data():
    return await marketwatch_get_performance("AAPL")

@pytest.mark.asyncio(scope="session")
async def test_type(data):
     assert type(data) == dict

@pytest.mark.asyncio(scope="session")
async def test_length(data):
    assert len(data) == 5

@pytest.mark.asyncio(scope="session")
async def test_fields_present(data):
    validator = pydantic.TypeAdapter(MarketwatchRecord)
    validator.validate_python(data)

@pytest.mark.asyncio(scope="session")
async def test_field_values_contain_pct(data):
    assert all(v.endswith('%') for v in data.values())

@pytest.mark.asyncio(scope="session")
async def test_no_alphabetic_and_spaces(data):
    assert not any(v.isupper() or v.islower() or ' ' in v for v in data.values())