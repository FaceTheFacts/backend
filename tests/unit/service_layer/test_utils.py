# third-party
from sqlalchemy import text

# local
from src.api import repository
from src.service_layer import utils
from src.db import models


class TestUtils:
    def test_fetch_missing_parties(
        self, postgres_session, setup_postgres_party_related_tables
    ):
        """Test handler for fetching missing parties from API"""
        # Arrange
        factory = repository.SqlAlchemyFactory(postgres_session)
        repo = factory.create_party_repository()
        # Act
        result = utils.FetchMissingEntity("parties", repo).fetch_missing_entities()
        # Assert
        assert isinstance(result, list)
        assert len(result[0]) != 0

    def test_fetch_missing_parties_with_no_update(self, postgres_session, setup_postgres_party_related_tables):
        """Test command handler for fetching missing parties from API"""
        # Arrange
        current_last_party_in_abgeordnetenwatch = {
            "id": 228,
            "entity_type": "party",
            "label": "Wählergruppe Solidaritätsbewegung",
            "api_url": "https://www.abgeordnetenwatch.de/api/v2/parties/228",
            "full_name": "Wählergruppe Solidaritätsbewegung (Solibew)",
            "short_name": "Wählergruppe Solidaritätsbewegung",
        }
        postgres_session.add(
            models.Party(
                id=current_last_party_in_abgeordnetenwatch["id"],
                entity_type=current_last_party_in_abgeordnetenwatch["entity_type"],
                label=current_last_party_in_abgeordnetenwatch["label"],
                api_url=current_last_party_in_abgeordnetenwatch["api_url"],
                full_name=current_last_party_in_abgeordnetenwatch["full_name"],
                short_name=current_last_party_in_abgeordnetenwatch["short_name"],
                party_style_id=1,
            )
        )
        factory = repository.SqlAlchemyFactory(postgres_session)
        repo = factory.create_party_repository()
        # Act
        result = utils.FetchMissingEntity("parties", repo).fetch_missing_entities()
        # Assert
        assert isinstance(result, list)
        assert result == []