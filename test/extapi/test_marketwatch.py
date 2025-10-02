import pydantic
import pytest

from extapi.marketwatch import marketwatch_get_performance
from models.marketwatch_record import MarketwatchRecord


@pytest.fixture(scope='module')
async def data():
    yield await marketwatch_get_performance("AAPL")

def test_type(data):
     assert type(data) == dict

def test_length(data):
    assert len(data) == 5

def test_fields_present(data):
    validator = pydantic.TypeAdapter(MarketwatchRecord)
    validator.validate_python(data)

def test_field_values_contain_pct(data):
    assert all(v.endswith('%') for v in data.values())

def test_no_alphabetic_and_spaces(data):
    assert not any(v.isupper() or v.islower() or ' ' in v for v in data.values())