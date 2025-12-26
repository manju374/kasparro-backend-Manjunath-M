import requests
import json

# --- CONFIGURATION ---
COINPAPRIKA_KEY = "YOUR_COINPAPRIKA_KEY_HERE"
COINGECKO_KEY = "YOUR_COINGECKO_KEY_HERE"

def test_coinpaprika():
    print("Testing CoinPaprika...")
    url = "https://api.coinpaprika.com/v1/coins/btc-bitcoin"
    
    # CoinPaprika Authentication: usually 'Authorization' header for some plans,
    # but the free tier is often open. However, the assignment insists on using the key.
    # Try passing it as a header.
    headers = {
        "Authorization": f"{COINPAPRIKA_KEY}" 
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ CoinPaprika Success!")
            print(f"Data Sample: {response.json()['name']} (${response.json().get('symbol')})")
        else:
            print(f"❌ CoinPaprika Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ CoinPaprika Error: {e}")

def test_coingecko():
    print("\nTesting CoinGecko...")
    # Authentication via Query Parameter (More reliable for testing)
    # Note: Use underscores 'x_cg_demo_api_key' for query params, not dashes.
    params = {
        "x_cg_demo_api_key": COINGECKO_KEY 
    }
    
    url = "https://api.coingecko.com/api/v3/ping"
    
    try:
        # Pass 'params' instead of 'headers'
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("✅ CoinGecko Success!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ CoinGecko Failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ CoinGecko Error: {e}")