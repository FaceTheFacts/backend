import datetime
import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.db.models.party_donation import PartyDonation
from src.db.models.party import Party
from src.db.models.party_style import PartyStyle
from src.db.models.party_donation_organization import PartyDonationOrganization

client = TestClient(app)


class TestPartyDonations:
    endpoint = "/partydonations"

    def test_v1_get_party_donations(self, setup_postgres_party_related_tables):
        """Test that the endpoint returns all party donations"""
        response = client.get("/v1" + self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 4
        # Assert party donation
        assert response.json()[0]["id"] == 4
        assert response.json()[0]["amount"] == 1000.0
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

    def test_plugin__get_party_donations_with_party_ids(
        self, setup_postgres_party_related_tables
    ):
        party_ids = [1, 100]
        response = client.get(
            "/plugin"
            + self.endpoint
            + f"?filters={party_ids[0]}"
            + f"&filters={party_ids[1]}"
        )
        # Assert
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2
        # Assert that the response is sorted by date
        assert response.json()["items"][0]["date"] == "2021-01-01"
        assert response.json()["items"][-1]["date"] == "2020-01-01"

    def test_plugin__get_party_donations_with_invalid_party_id(
        self, setup_postgres_party_related_tables
    ):
        party_ids = [100]
        response = client.get("/plugin" + self.endpoint + f"?filters={party_ids[0]}")
        # Assert
        assert response.status_code == 404

    def test_plugin__get_party_donations_without_party_ids(
        self, setup_postgres_party_related_tables
    ):
        party_ids = [1, 100]
        response = client.get("/plugin" + self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(response.json()["items"]) == 4
        # Assert that the response is sorted by date
        assert response.json()["items"][0]["date"] == "2023-01-01"
        assert response.json()["items"][-1]["date"] == "2020-01-01"


class TestParty:
    endpoint = "/parties"

    def test_v1_parties(self, setup_postgres_party_related_tables):
        response = client.get("/plugin" + self.endpoint)
        # Assert
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 4
        # Assert that the response is sorted by party_id
        assert items[0]["id"] == 1
        assert items[-1]["id"] == 4
