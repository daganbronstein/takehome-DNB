# StocksAPI Service

## Overview

StocksAPI is a small, FastAPI service that makes use of a Redis backend to cache and
present data persisted from external sources, including Polygon and Marketwatch.

Largely functional and minimalistic, its focus is on presenting an easy-to-use
interface to the capabilities it exports. The meat of the business logic
is located in src/classes/stocks_service.py, src/extapi/marketwatch.py,
and src/extapi/polygon.py

You will find the caching/DB layer in src/classes/cache.py, and all FastAPI logic
in src/main.py and src/api/stock_router.py.

Models for FastAPI validation can be found in src/api/models, and TypedDicts for
representing the interface with external sources and DB models can be found in
src/models.

Tests can be found in test/, and they largely focus on integration, with minimal mocking.
Their focus is assuring that the DB is being correctly used, and that the scraper
and Polygon API consumer have not had their contracts unilaterally changed by the
external source.


## Setup

1. **Build the container**:
    ```bash
   docker build --tag "stocks-api" .
    ```
2. Run the container with the Polygon API key
    ```bash
   docker run --name StocksAPI -p 8000:8000 -e POLYGON_API_KEY="key" stocks-api 
    ```
   
## Usage

### Fetching Stock information
```bash 
curl -i -H "Content-Type: application/json" -X GET http://localhost:8000/stock/AAPL  
```

### Updating held stocks
```bash 
curl -H "Content-Type: application/json" --data '{"amount":5}' http://localhost:8000/stock/AAPL
```


