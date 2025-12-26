import requests
from app.core.config import settings

BASE_URL = "https://api.coinpaprika.com/v1"

def fetch_coin_ticker(coin_id: str = "btc-bitcoin"):
    """
    Fetches ticker data (price, volume) for a specific coin.
    """
    url = f"{BASE_URL}/tickers/{coin_id}"
    
    # Using the key as verified in your smoke test
    headers = {}
    if settings.COINPAPRIKA_API_KEY:
        headers["Authorization"] = settings.COINPAPRIKA_API_KEY

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise error for 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinPaprika: {e}")
        return None