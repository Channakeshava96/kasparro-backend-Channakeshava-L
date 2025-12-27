import httpx
import pytest

# The base URL for your running API
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Tests if the /health endpoint is working."""
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["database"] == "connected"
        assert "last_etl_run" in data

def test_get_data_no_filters():
    """Tests the /data endpoint without any filters."""
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/data")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert "total_records" in data
        assert "data" in data

def test_get_data_with_filters():
    """Tests the filtering capabilities of the /data endpoint."""
    with httpx.Client() as client:
        # Test filtering by coin
        response = client.get(f"{BASE_URL}/data?coin=BTC")
        assert response.status_code == 200
        for record in response.json()["data"]:
            assert record["coin"] == "BTC"

        # Test filtering by source
        response = client.get(f"{BASE_URL}/data?source=csv")
        assert response.status_code == 200
        for record in response.json()["data"]:
            assert record["source"] == "csv"