import datetime
import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.e2e
class TestPartyDonations:
    endpoint = "/plugin/partydonations"

    def test_get_party_donations_with_party_ids(
        self, setup_postgres_party_related_tables
    ):
        """Test that the endpoint returns the correct data for the given party ids."""
        party_ids = [1, 100]
        response = client.get(
            self.endpoint + f"?filters={party_ids[0]}" + f"&filters={party_ids[1]}"
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
        # Assert that the response is sorted by date
        assert response.json()["items"][0]["date"] == "2021-01-01"
        assert response.json()["items"][-1]["date"] == "2020-01-01"

    def test_get_party_donations_with_invalid_party_id(
        self, setup_postgres_party_related_tables
    ):
        """Test that the endpoint returns 404 if the party id is invalid."""
        party_ids = [100]
        response = client.get(self.endpoint + f"?filters={party_ids[0]}")
        # Assert
        assert response.status_code == 404

    def test_get_party_donations_without_party_ids(
        self, setup_postgres_party_related_tables
    ):
        """Test that the endpoint returns the correct data."""
        party_ids = [1, 100]
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(response.json()["items"]) == 4
        # Assert that the response is sorted by date
        assert response.json()["items"][0]["date"] == "2023-01-01"
        assert response.json()["items"][-1]["date"] == "2020-01-01"


@pytest.mark.e2e
class TestParty:
    endpoint = "/plugin/parties"

    def test_get_parties(self, setup_postgres_party_related_tables):
        """Test that the endpoint returns the correct data."""
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 4
        # Assert that the response is sorted by party_id
        assert items[0]["id"] == 1
        assert items[-1]["id"] == 4
