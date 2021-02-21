from typing import Any

from core.errors import GetStockException
from fastapi import APIRouter, HTTPException
from loguru import logger
from models.stocktrade import StockInsiderResponse, StockFundamentalsResponse, StockNewsResponse
from services.stock import StockTraderHandler as stocks

router = APIRouter()


@router.get("/insider/", response_model=StockInsiderResponse, name="insider:get-ticker")
async def insider(ticker_input: str = None):
    if not ticker_input:
        raise HTTPException(status_code=404, detail=f"'ticker_input' argument invalid!")

    try:
        insider_df = stocks.get_insider_df(ticker_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return StockInsiderResponse(insider_df=insider_df)


@router.get("/fundamentals/", response_model=StockFundamentalsResponse, name="fundamentals:get-ticker")
async def fundamentals(ticker_input: str = None):
    if not ticker_input:
        raise HTTPException(status_code=404, detail=f"'ticker_input' argument invalid!")

    try:
        fundamentals_df = stocks.get_fundamentals(ticker_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return StockFundamentalsResponse(fundamentals_df=fundamentals_df)


@router.get("/news/", response_model=StockNewsResponse, name="news:get-ticker")
async def insider(ticker_input: str = None):
    if not ticker_input:
        raise HTTPException(status_code=404, detail=f"'ticker_input' argument invalid!")

    try:
        news_df = stocks.get_news(ticker_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")

    return StockNewsResponse(news_df=news_df)
