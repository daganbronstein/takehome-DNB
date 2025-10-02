import pytest

from classes.cache import CacheService

@pytest.fixture(scope="module")
def true_cache():
    """Gives an instance of a true CacheService (redis, not fakeredis), and empties it completely at end of scope. """
    cache = CacheService()
    yield cache
    cache.clear()
