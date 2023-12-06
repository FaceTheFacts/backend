# std
import json
import time

# third-party
from sqlalchemy import text
import pytest

# local
from src.entrypoints import (
    redis_utils,
    redis_eventpublisher,
    redis_eventconsumer_missing_entity_fetched,
    redis_eventconsumer_update_data_prepared,
)


def wait_for_messages(pubsub, timeout):
    start_time = time.time()
    messages = []
    while time.time() - start_time < timeout:
        message = pubsub.get_message(timeout=1)
        if message:
            messages.append(message)

    return messages


# Turn on redis-server before running the tests
@pytest.mark.e2e
class TestPipeline:
    """Test the Redis event pipeline."""

    def setup_method(self):
        """Setup the Redis event pipeline."""
        self.redis_client = redis_utils.RedisClient(host="localhost", port=6379)
        self.pubsub_missing_entity = self.redis_client.pubsub()
        self.pubsub_updated_entity = self.redis_client.pubsub()

        self.pubsub_missing_entity.subscribe("missing_entity_fetched")
        self.pubsub_updated_entity.subscribe("updated_entity_prepared")

    def cleanup(self):
        """Cleanup the Redis event pipeline."""
        self.session.execute(text("DELETE FROM party_style"))
        self.session.execute(text("DELETE FROM party"))

    def test_fetch_missing_entity_from_third_party_api(self, session):
        """Test fetching missing entity from third-party API. (step 1)"""
        self.session = session
        entity = "party"
        # Act
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=self.redis_client
        )

        messages = wait_for_messages(self.pubsub_missing_entity, timeout=3)
        data = json.loads(messages[-1]["data"])
        # Assert
        assert data["entity"] == entity
        assert len(data["data"]) != 0

    def test_subscribe_updated_entity_prepared(self, session):
        """Test subscribing to updated_entity_prepared event. (step 1 and step 2)"""
        self.session = session
        entity = "party"
        # Act
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=self.redis_client
        )

        messages_missing_entity = wait_for_messages(
            self.pubsub_missing_entity, timeout=3
        )

        for message in messages_missing_entity:
            redis_eventconsumer_missing_entity_fetched.handle_message(message=message)

        messages_updated_entity = wait_for_messages(
            self.pubsub_updated_entity, timeout=3
        )

        data = json.loads(messages_updated_entity[-1]["data"])
        # Assert
        assert data["entities"] == ["party_style", "party"]
        assert len(data["data"]) == 2

    def test_update_data_with_third_party_api_data(self, session):
        """Test updating data with third-party API data. (step 1, step 2 and step 3)"""
        self.session = session
        entity = "party"
        # Act
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=self.redis_client
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
                message=message, session=session
            )

        rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 220})
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
        # Cleanup
        self.cleanup()
