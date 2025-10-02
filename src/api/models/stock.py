from pydantic import BaseModel, Field

from models.marketwatch_record import MarketwatchRecord


class StockModel(BaseModel):
    afterHours: float
    close: float
    from_: str = Field(serialization_alias="from")
    high: float
    low: float
    open: float
    preMarket: float
    status: str
    symbol: str
    volume: int
    performance: MarketwatchRecord | None
    amount: int