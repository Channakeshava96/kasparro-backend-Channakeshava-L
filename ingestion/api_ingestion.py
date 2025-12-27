import httpx
from core.config import get_settings

COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/tickers"

def fetch_coinpaprika_data():
    settings = get_settings()

    headers = {
        "Authorization": f"Bearer {settings.coinpaprika_api_key}"
    }

    response = httpx.get(
        COINPAPRIKA_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.json()
