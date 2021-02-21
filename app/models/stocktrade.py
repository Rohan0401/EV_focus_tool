from pydantic import BaseModel
from typing import List, Any, Dict


class StockInsiderResponse(BaseModel):
    insider_df: List[Any]


class StockFundamentalsResponse(BaseModel):
    fundamentals_df: Dict


class StockNewsResponse(BaseModel):
    news_df: List[Any]
