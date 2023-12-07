# third-party
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

# local
from src.api.main import app
from src.entrypoints import (
    redis_eventconsumer_missing_entity_fetched,
    redis_eventconsumer_update_data_prepared,
    redis_eventpublisher,
    redis_utils,
)
from src.db.models.party import Party
from src.db.models.party_style import PartyStyle
from tests.unit.entrypoints.test_external_events import wait_for_messages

client = TestClient(app)


# Turn on redis-server before running the tests
@pytest.mark.e2e
class TestParty:
    """Test that the endpoint returns the correct data."""

    def setup_method(self):
        """Setup the Redis event pipeline."""
        self.redis_client = redis_utils.RedisClient(host="localhost", port=6379)
        self.pubsub_missing_entity = self.redis_client.pubsub()
        self.pubsub_updated_entity = self.redis_client.pubsub()

        self.pubsub_missing_entity.subscribe("missing_entity_fetched")
        self.pubsub_updated_entity.subscribe("updated_entity_prepared")

    def cleanup(self):
        """Cleanup the DB."""
        self.session.query(Party).delete()
        self.session.query(PartyStyle).delete()
        self.session.commit()

    def test_get_parties(self, postgres_session):
        # Arrange
        page = 1
        size = 25
        self.endpoint = f"/plugin/parties?page={page}&size={size}"
        self.session = postgres_session
        entity = "party"
        # Act - Fetch missing data -> Update tables
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=postgres_session, redis_client=self.redis_client
        )

        messages_missing_entity = wait_for_messages(
            self.pubsub_missing_entity, timeout=3
        )

        for message in messages_missing_entity:
            redis_eventconsumer_missing_entity_fetched.handle_message(message=message)

        messages_updated_entity = wait_for_messages(
            self.pubsub_updated_entity, timeout=3
        )

        for message in messages_updated_entity:
            redis_eventconsumer_update_data_prepared.handle_message(
                message=message, session=postgres_session
            )

        rows = postgres_session.execute(
            text("SELECT * FROM party WHERE id = :id"), {"id": 220}
        )
        # Assert
        assert list(rows) == [
            (
                220,
                "party",
                "Bündnis Deutschland",
                "https://www.abgeordnetenwatch.de/api/v2/parties/220",
                "Bündnis Deutschland",
                "Bündnis Deutschland",
                220,
            )
        ]
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == page * size
        # Assert that the response is sorted by party_id
        assert items[0]["id"] == page * size - size + 1
        assert items[-1]["id"] == page * size

        # Cleanup
        self.cleanup()
