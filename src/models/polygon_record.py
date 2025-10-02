from typing import TypedDict


class PolygonRecord(TypedDict):
    status: str
    from_: str
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    afterHours: float
    preMarket: float