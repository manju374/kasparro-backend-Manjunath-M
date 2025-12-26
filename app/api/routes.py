import time
import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import CryptoMarketData, RawData
from app.schemas import PaginatedResponse, Metadata

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # P0.2 Req: Check DB connectivity
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

@router.get("/data", response_model=PaginatedResponse)
def get_market_data(
    symbol: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    # Query Database
    query = db.query(CryptoMarketData)
    
    # Filter
    if symbol:
        query = query.filter(CryptoMarketData.symbol == symbol.upper())
    
    # Pagination
    data = query.offset(offset).limit(limit).all()
    
    # Metadata
    process_time = (time.time() - start_time) * 1000
    
    return {
        "data": data,
        "metadata": {
            "request_id": str(uuid.uuid4()),
            "api_latency_ms": round(process_time, 2)
        }
    }
