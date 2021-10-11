from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_country():
    response = client.get("/country/61")
    assert response.status_code == 200
    assert response.json() == {"id": 61, "label": "Deutschland"}


def test_read_country_not_existing_id():
    response = client.get("/country/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}
