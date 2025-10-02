import os
from datetime import date

import requests

from classes.cache import CacheService
from enums.cache_keys import CacheKeys
from extapi.exceptions.polygon_exceptions import PolygonGenericException, PolygonConnectionError, PolygonJSONError
from models.polygon_record import PolygonRecord

POLYGON_API = "https://api.polygon.io/v1/open-close/{symbol}/{date}"
POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY", "MISSING")

async def polygon_get_stocks(symbol: str, _date: date) -> PolygonRecord:
    r"""Fetches the status of the stock from Polygon.

    :param symbol: The company stock symbol that will be queried
    :param _date: The specific date that will be fetched
    :return: parsed response from Polygon
    :raises PolygonGenericException: if polygon is down, we can"t connect to it, or Polygon returned an error.
    """

    # TODO there is a race here
    #  if multiple requests to the same key arrive too quickly, we will have several unnecessary misses (because
    #  networking operations are not blocking, i.e. the call to _fetch). Consider a lock with shared reads and exclusive
    #  writes if using redis-aio.

    # make use of caching; we have limited API calls
    cache_key = _get_cache_key(symbol, _date)
    result: PolygonRecord | None = CacheService().get_object(cache_key)
    if result:
        return result

    result = await _fetch(POLYGON_API_KEY, symbol, _date)
    CacheService().set_object(cache_key, result)

    # TODO additional enrichment/transformations?

    return result

def _get_cache_key(symbol: str, _date: date) -> str:
    return f"{CacheKeys.POLYGON}:{symbol}:${_date.strftime("%Y-%m-%d")}"

async def _fetch(api_key: str, symbol: str, _date: date) -> PolygonRecord:
    try:
        response = requests.get(
            POLYGON_API.format(symbol=symbol, date=_date.strftime("%Y-%m-%d")),
            headers={
                "Authorization": f"Bearer {api_key}"
        })

        # Polygon API guarantees all responses to be presented in JSON, including failures.
        content = response.json()

        if content.get("status", "ERROR") == "ERROR":
            raise PolygonGenericException("Polygon returned an API error", data=content)

        # Hack; need to look further into this, no time to do so
        content["from_"] = content["from"]

        return content
    except requests.ConnectionError as err:
        raise PolygonConnectionError("Failed to connect to Polygon API", exception=err)
    except requests.exceptions.JSONDecodeError as err:
        raise PolygonJSONError("Polygon API returned malformed response", exception=err)
    except Exception as err:
        raise PolygonGenericException("An unknown exception was raised when calling Polygon API", exception=err)
