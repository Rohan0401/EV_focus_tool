from fastapi import APIRouter

from app.api.routes import predictor, stocks

router = APIRouter()
# router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(stocks.router, tags=["insider"], prefix="/v1")
