import datetime
import logging
import os
import threading
from typing import Any, TypeVar

import fakeredis
import redis
from redis.lock import Lock

from enums.cache_keys import CacheKeys

logger = logging.getLogger(__name__)
T = TypeVar("T")
SEVEN_DAYS = 604800

class CacheService:
    _instance: 'CacheService' = None
    _lock: threading.Lock = threading.Lock()
    rc: redis.Redis

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(CacheService, cls).__new__(cls)
                    cls._connect(cls._instance)
        return cls._instance

    def _connect(self) -> None:
        try:
            if os.environ.get("USE_FAKEREDIS", False):
                self.rc = fakeredis.FakeRedis()
            else:
                self.rc = redis.Redis(host='localhost', port=6379, decode_responses=True)
            logger.info("Connected to fakeredis server")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

    # TODO reconnect

    def is_connected(self) -> bool:
        try:
            self.rc.ping()
        except redis.ConnectionError:
            return False

        return True

    def assert_connected(self) -> None:
        if not self.rc or not self.is_connected():
            # TODO do proper exception, but this really shouldn't happen
            raise Exception("Attempted to interact with not initialized Redis client")

    def clear(self) -> None:
        # TODO only for tests, but quite inefficient! We should use a pipeline, and we should also
        #   add safeguards so that this is not accidently run against production redis (such as prefix test: to all keys)

        # mypy complains. There's an issue with the annotations, this is not an Awaitable.
        for key in self.rc.keys():
            self.rc.delete(key)

    def lock(self, lock_name: str, timeout: float | None = None) -> Lock:
        """Acquires a lock, should be used to prevent race conditions. If the issue is a race between individual steps,
        consider a pipeline."""

        # This returns a redis.Lock directly to the user, which is not a great idea for maintainability.
        #  Better return a local CacheLock with a contract that we define, not Redis.
        return self.rc.lock(f"{CacheKeys.LOCK}:{lock_name}", timeout)

    def get_value(self, key: str) -> str:
        """Fetches a record stored as a simple value (str, int, float), but will always return it as a string."""
        self.assert_connected()

        # TODO mypy claims this is awaitable, the result is not awaitable. Typings assume aio-redis installed or
        #  something? Not entirely sure, need to look further into this
        return str(self.rc.get(key) or "")

    def set_value(self, key: str, value: str | int | float, expires: int = 0) -> None:
        """
        Stores a simple value. Even if a float or int is provided, it will be returned as a string later.
        TODO We can consider storing the type of the value as part of the key, and then use a converter to restore it.

        :param key: key of the stored record
        :param value: value (will become string if it isn't)
        :param expires: Time in seconds to maintain the record. Default is 0, which will apply a 7d TTL
        """
        self.rc.set(key, value, datetime.timedelta(seconds=expires or SEVEN_DAYS))


    def get_object(self, key: str) -> Any:
        """
        Fetches a record stored as a structured value and returns a dict.

        :return: dict of the stored object. Empty if not present
        """

        # Annoyingly, must return Any for now. There are solutions.
        return self.rc.hgetall(key)

    def set_object(self, key: str, value: Any, expires: int = 0) -> None:
        """
        Stores a dict as a record in the cache. If already present, will overwrite

        :param key: key of the stored record
        :param value: value (currently only dicts supported)
        :param expires: Time in seconds to maintain the record. Default is 0, which will apply a 7d TTL
        """
        self.rc.hset(key, mapping=value)
        self.rc.expire(key, datetime.timedelta(seconds=expires or SEVEN_DAYS))
