from unittest import mock

import pydantic
import pytest

from extapi.polygon import polygon_get_stocks, PolygonConnectionError
from models.polygon_record import PolygonRecord


async def test_req_get_stocks(yesterday, monkeypatch):
    """
    A single unit test that actually calls the API, confirming that fetch() works
     and that the desired fields are present. Moving forward, we will be mocking the results in other tests.
    """

    # There is a limit of something like 5 requests per minute. Bear this in mind when executing this test.
    res = await polygon_get_stocks("AAPL", yesterday)

    validator = pydantic.TypeAdapter(PolygonRecord)
    validator.validate_python(res)


@mock.patch('extapi.polygon.POLYGON_API', 'http://0.0.0.0')
async def test_fetch_badurl(yesterday):
    with pytest.raises(PolygonConnectionError) as e:
        await polygon_get_stocks("ABCD", yesterday)


# Add a test setting up a local fake URL that returns non-JSON data so that we can test PolygonJSONError
