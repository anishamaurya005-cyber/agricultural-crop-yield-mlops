
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_predict():
    payload = {
        "area": "Albania",
        "year": 2013,
        "average_rain_fall_mm_per_year": 1485.0,
        "pesticides_tonnes": 121.0,
        "avg_temp": 16.0,
        "item": "Maize"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "predicted_yield_hg_ha" in response.json()
    assert isinstance(
        response.json()["predicted_yield_hg_ha"], (int, float)
    )


def test_predict_missing_field():
    payload = {
        "area": "Albania",
        "year": 2013,
        "item": "Maize"
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422