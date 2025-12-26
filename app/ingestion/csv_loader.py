import csv
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import CryptoMarketData, RawData

def load_csv_data(file_path: str = "historical_data.csv"):
    print(f"--- Loading CSV: {file_path} ---")
    
    db = SessionLocal()
    try:
        with open(file_path, mode="r") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                # 1. Transform CSV row to DB Model
                market_record = CryptoMarketData(
                    symbol=row["symbol"],
                    name=row["name"],
                    price_usd=float(row["price_usd"]),
                    market_cap_usd=float(row["market_cap"]),
                    volume_24h_usd=float(row["volume_24h"]),
                    source="csv_upload"
                )
                
                # 2. Save Raw Data (Audit) - P0.1 Requirement
                raw_record = RawData(
                    source="csv",
                    endpoint=file_path,
                    raw_payload=row
                )
                
                db.add(raw_record)
                db.add(market_record)
                count += 1
            
            db.commit()
            print(f"Successfully loaded {count} records from CSV.")
            
    except Exception as e:
        print(f"Error loading CSV: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_csv_data()
