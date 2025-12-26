from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CryptoDataResponse(BaseModel):
    symbol: str
    name: str
    price_usd: float
    market_cap_usd: float
    volume_24h_usd: float
    source: str
    fetched_at: datetime
    class Config:
        from_attributes = True

class Metadata(BaseModel):
    request_id: str
    api_latency_ms: float

class PaginatedResponse(BaseModel):
    data: List[CryptoDataResponse]
    metadata: Metadata
