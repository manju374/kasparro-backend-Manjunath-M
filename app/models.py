from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class RawData(Base):
    """
    P0.1 Req: Store raw data into Postgres.
    This acts as an immutable log of everything we fetched.
    """
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # e.g., 'coinpaprika', 'coingecko', 'csv'
    endpoint = Column(String)            # e.g., '/coins/btc-bitcoin'
    raw_payload = Column(JSON)           # The exact JSON response
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False) # Has this been normalized yet?

class CryptoMarketData(Base):
    """
    P0.1 Req: Normalize into a unified schema.
    All sources (Paprika, Gecko, CSV) must be mapped to this format.
    """
    __tablename__ = "crypto_market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)   # e.g., BTC, ETH
    name = Column(String)                 # e.g., Bitcoin
    price_usd = Column(Float)
    market_cap_usd = Column(Float)
    volume_24h_usd = Column(Float)
    
    # Metadata
    source = Column(String)               # Where did this price come from?
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())