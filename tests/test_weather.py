import pytest
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

cities = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург"]

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.parametrize("city", cities)
def test_weather_route(city):
    response = client.post("/weather", data={"city": city})
    assert response.status_code == 200
    assert "Температура" in response.text or "Город не найден" in response.text