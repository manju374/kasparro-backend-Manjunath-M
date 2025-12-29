from fastapi import FastAPI
from app.api import routes
from app.core.database import engine, Base

# Create Tables on startup (failsafe)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kasparro Backend")

# --- CRITICAL FIX: Include the API Routes ---
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"status": "Kasparro Backend is Running"}
