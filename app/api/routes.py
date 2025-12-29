from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.models import CryptoMarketData

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Simple SQL query to verify connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        print(f"Health Check Error: {e}")
        # Even if this fails, the app might be okay, but we return 500 to be safe
        raise HTTPException(status_code=500, detail="Database connection failed")

@router.get("/data")
def get_market_data(
    limit: int = 10, 
    offset: int = 0, 
    symbol: str = None, 
    db: Session = Depends(get_db)
):
    query = db.query(CryptoMarketData)
    if symbol:
        query = query.filter(CryptoMarketData.symbol == symbol.upper())

    data = query.offset(offset).limit(limit).all()
    return {"data": data}