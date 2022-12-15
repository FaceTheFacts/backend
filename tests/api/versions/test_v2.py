from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_politician_route_ok_status_code():
    response = client.get("/v2/politician/28881")
    assert response.status_code == 200


# def test_politician_route_does_not_exist_status_code():
#     response = client.get("/v2/politician/0")
#     assert response.status_code == 404

# def test_politician_route_does_not_exist_message():
#     response = client.get("/v2/politician/0")
#     assert response.json() == {"detail": "Politician not found"}
