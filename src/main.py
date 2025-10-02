from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.stock_router import stock_router
from classes.app_exception import AppException

app = FastAPI()
app.include_router(stock_router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={'code': exc.error_code, 'message': exc.message}
    )
