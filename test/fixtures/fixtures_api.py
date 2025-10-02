from datetime import datetime, timedelta

import pytest_asyncio

@pytest_asyncio.fixture
def yesterday():
    return datetime.today() - timedelta(days=1)
