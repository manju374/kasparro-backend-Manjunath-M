from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.coinpaprika import fetch_coin_ticker
from app.services.coingecko import fetch_coingecko_data
from app.models import RawData, CryptoMarketData

def process_coinpaprika(db: Session):
    print("--- 1. Processing CoinPaprika ---")
    data = fetch_coin_ticker("btc-bitcoin")
    if not data: return

    # Save Raw
    db.add(RawData(source="coinpaprika", endpoint="tickers", raw_payload=data))
    
    # Save Clean
    db.add(CryptoMarketData(
        symbol=data.get("symbol"),
        name=data.get("name"),
        price_usd=data.get("quotes", {}).get("USD", {}).get("price"),
        market_cap_usd=data.get("quotes", {}).get("USD", {}).get("market_cap"),
        volume_24h_usd=data.get("quotes", {}).get("USD", {}).get("volume_24h"),
        source="coinpaprika"
    ))
    db.commit()
    print("   -> Saved CoinPaprika Data")

def process_coingecko(db: Session):
    print("--- 2. Processing CoinGecko ---")
    data = fetch_coingecko_data("bitcoin")
    if not data: return

    # Save Raw
    db.add(RawData(source="coingecko", endpoint="simple/price", raw_payload=data))

    # Save Clean (Normalize fields to match our schema)
    # CoinGecko returns: {"usd": 50000, "usd_market_cap": ...}
    db.add(CryptoMarketData(
        symbol="BTC",       # CoinGecko simple/price doesn't return symbol, so we hardcode or lookup
        name="Bitcoin",
        price_usd=data.get("usd"),
        market_cap_usd=data.get("usd_market_cap"),
        volume_24h_usd=data.get("usd_24h_vol"),
        source="coingecko"
    ))
    db.commit()
    print("   -> Saved CoinGecko Data")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        process_coinpaprika(db)
        process_coingecko(db)
    finally:
        db.close()