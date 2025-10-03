import asyncio

import pytest

from classes.cache import CacheService


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def true_cache(event_loop):
    """Gives an instance of a true CacheService (redis, not fakeredis), and empties it completely at end of scope. """
    cache = CacheService()
    yield cache
    await cache.clear()
    await cache.shutdown()
