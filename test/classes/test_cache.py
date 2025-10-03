import pytest

from classes.cache import CacheService

@pytest.mark.asyncio(scope="session")
async def test_value_store_string(true_cache: CacheService):
    await true_cache.is_connected()

    await true_cache.set_value("AStr", "B")
    stored_val = await true_cache.get_value("AStr")
    assert stored_val == "B"

@pytest.mark.asyncio(scope="session")
async def test_value_store_float(true_cache: CacheService):
    await true_cache.is_connected()

    await true_cache.set_value("AFloat", 1.0)
    stored_val = await true_cache.get_value("AFloat")
    assert stored_val == "1.0"


@pytest.mark.asyncio(scope="session")
async def test_value_store_int(true_cache: CacheService):
    await true_cache.is_connected()

    await true_cache.set_value("AInt", 1)
    stored_val = await true_cache.get_value("AInt")
    assert stored_val == "1"

@pytest.mark.asyncio(scope="session")
async def test_object_store(true_cache: CacheService):
    await true_cache.is_connected()

    await true_cache.set_object("AObj", {"A": "B"})
    stored_obj = await true_cache.get_object("AObj")
    assert "A" in stored_obj
    assert type(stored_obj) is dict
    assert "B" == stored_obj["A"]

# TODO expiry tests
