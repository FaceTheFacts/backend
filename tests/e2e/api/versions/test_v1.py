import datetime
import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.e2e
class TestPartyDonations:
    endpoint = "/v1/partydonations"

    def test_get_party_donations(self, setup_postgres_party_related_tables):
        """Test that the endpoint returns all party donations"""
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 4
        # Assert party donation
        assert response.json()[0]["id"] == 4
        assert response.json()[0]["date"] == "2023-01-01"
        # Assert party
        assert response.json()[0]["party"]["id"] == 2
        assert response.json()[0]["party"]["label"] == "SPD"
        # Assert party style
        assert response.json()[0]["party"]["party_style"]["id"] == 2
        assert response.json()[0]["party"]["party_style"]["display_name"] == "SPD"

        # Assert party donation organization
        assert response.json()[0]["party_donation_organization"]["id"] == 4
        assert (
            response.json()[0]["party_donation_organization"]["donor_name"]
            == "Friede Springer"
        )
        # Assert that the response is sorted by date
        assert response.json()[0]["date"] == "2023-01-01"
        assert response.json()[-1]["date"] == "2020-01-01"
