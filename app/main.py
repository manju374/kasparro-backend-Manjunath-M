from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.core.database import engine

app = FastAPI()

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        print("HEALTH CHECK ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Database connection failed")
