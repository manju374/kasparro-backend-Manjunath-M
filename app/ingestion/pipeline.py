from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.coinpaprika import fetch_coin_ticker
from app.services.coingecko import fetch_coingecko_data
from app.models import RawData, CryptoMarketData

def normalize_and_store(db: Session, source: str, raw_data: dict):
    """
    Unified logic to normalize data from any source into the CryptoMarketData schema.
    """
    clean_record = None

    if source == "coinpaprika":
        # Normalization Logic for CoinPaprika
        clean_record = CryptoMarketData(
            symbol=raw_data.get("symbol", "UNKNOWN"),
            name=raw_data.get("name", "Unknown"),
            price_usd=raw_data.get("quotes", {}).get("USD", {}).get("price"),
            market_cap_usd=raw_data.get("quotes", {}).get("USD", {}).get("market_cap"),
            volume_24h_usd=raw_data.get("quotes", {}).get("USD", {}).get("volume_24h"),
            source=source
        )
    
    elif source == "coingecko":
        # Normalization Logic for CoinGecko (Manual Mapping required)
        # CoinGecko simple/price doesn't give symbol/name, so we map the ID 'bitcoin' -> 'BTC'
        symbol_map = {"bitcoin": "BTC", "ethereum": "ETH"}
        # 'raw_data' here is just the inner dict: {'usd': 96000, ...}
        
        clean_record = CryptoMarketData(
            symbol="BTC", # Normalized
            name="Bitcoin",
            price_usd=raw_data.get("usd"),
            market_cap_usd=raw_data.get("usd_market_cap"),
            volume_24h_usd=raw_data.get("usd_24h_vol"),
            source=source
        )

    if clean_record:
        db.add(clean_record)
        db.commit()

def process_pipeline():
    db = SessionLocal()
    try:
        # 1. CoinPaprika
        print("--- Processing CoinPaprika ---")
        cp_data = fetch_coin_ticker("btc-bitcoin")
        if cp_data:
            db.add(RawData(source="coinpaprika", endpoint="tickers", raw_payload=cp_data))
            normalize_and_store(db, "coinpaprika", cp_data)
            print(" -> CoinPaprika Data Saved")

        # 2. CoinGecko
        print("--- Processing CoinGecko ---")
        cg_data = fetch_coingecko_data("bitcoin")
        if cg_data:
            db.add(RawData(source="coingecko", endpoint="simple/price", raw_payload=cg_data))
            normalize_and_store(db, "coingecko", cg_data)
            print(" -> CoinGecko Data Saved")
            
    except Exception as e:
        print(f"Pipeline Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    process_pipeline()
