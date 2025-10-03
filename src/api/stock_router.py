from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.models.stock import StockModel
from classes.stocks_service import StocksService
from extapi.marketwatch import marketwatch_get_performance
from extapi.polygon import polygon_get_stocks
from models.marketwatch_record import MarketwatchRecord
from models.polygon_record import PolygonRecord

stock_router = APIRouter(prefix="/stock")

class UpdateStockRequest(BaseModel):
    amount: int

@stock_router.post("/{stock_symbol}", status_code=201)
async def update_stock(stock_symbol: str, update: UpdateStockRequest) -> str:
    # Slightly more detailed handling than described. These are what-if cases that normally, if
    #   absent from the story, I'd ask the product. Saw no point in emailing over this,
    #   so went with what I thought reasonable.
    if not update.amount:
        raise HTTPException(status_code=400, detail="You must insert a valid amount.")

    await StocksService().add_stock(stock_symbol, update.amount)

    if update.amount < 0:
        return f"{-update.amount} units of stock {stock_symbol} were removed from your stock record."
    else:
        return f"{update.amount} units of stock {stock_symbol} were added to your stock record."


@stock_router.get("/{stock_symbol}")
async def get_stock(stock_symbol: str) -> StockModel:
    mw_record: MarketwatchRecord | None = await marketwatch_get_performance(stock_symbol)
    pg_record: PolygonRecord = await polygon_get_stocks(stock_symbol, datetime.today() - timedelta(days=1))

    stock_amount: int = await StocksService().get_stock_amount(stock_symbol)

    response: StockModel = StockModel(
        afterHours=pg_record["afterHours"],
        close=pg_record["close"],
        from_=pg_record["from_"],
        high=pg_record["high"],
        low=pg_record["low"],
        open=pg_record["open"],
        preMarket=pg_record["preMarket"],
        status=pg_record["status"],  # don't think we need this? This is the request status I think, but is explicitly req
        symbol=pg_record["symbol"],
        volume=pg_record["volume"],
        performance=mw_record,
        amount=stock_amount,
    )

    return response