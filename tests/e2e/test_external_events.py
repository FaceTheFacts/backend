# std
import json
import time
from sqlalchemy import text

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


class TestPipeline:
    def test_fetch_missing_entity_from_third_party_api(self, session):
        redis_client = redis_utils.RedisClient(host="localhost", port=6379)
        pubsub = redis_client.pubsub()
        # Arrange
        pubsub.subscribe("missing_entity_fetched")  # Subscribe to channel 1

        # Act
        entity = "party"
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=redis_client
        )
        messages = wait_for_messages(pubsub, timeout=3)
        data = json.loads(messages[-1]["data"])

        # Assert
        assert data["entity"] == entity
        assert len(data["data"]) != 0

    def test_subscribe_updated_entity_prepared(self, session):
        redis_client = redis_utils.RedisClient(host="localhost", port=6379)

        # Create separate pubsub instances for each channel
        pubsub_missing_entity = redis_client.pubsub()
        pubsub_updated_entity = redis_client.pubsub()

        # Arrange
        pubsub_missing_entity.subscribe("missing_entity_fetched")
        pubsub_updated_entity.subscribe("updated_entity_prepared")

        # Act
        entity = "party"

        # Publish messages to the "missing_entity_fetched" channel
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=redis_client
        )

        # Wait for messages on the "missing_entity_fetched" channel
        messages_missing_entity = wait_for_messages(pubsub_missing_entity, timeout=3)

        # Handle messages on the "missing_entity_fetched" channel
        for message in messages_missing_entity:
            redis_eventconsumer_missing_entity_fetched.handle_message(message=message)

        # Wait for messages on the "updated_entity_prepared" channel
        messages_updated_entity = wait_for_messages(pubsub_updated_entity, timeout=3)

        data = json.loads(messages_updated_entity[-1]["data"])
        # Assert
        assert data["entities"] == ["party_style", "party"]
        assert len(data["data"]) == 2

    def test_update_data_with_third_party_api_data(self, session):
        redis_client = redis_utils.RedisClient(host="localhost", port=6379)

        # Create separate pubsub instances for each channel
        pubsub_missing_entity = redis_client.pubsub()
        pubsub_updated_entity = redis_client.pubsub()

        # Arrange
        pubsub_missing_entity.subscribe("missing_entity_fetched")
        pubsub_updated_entity.subscribe("updated_entity_prepared")

        # Act
        entity = "party"

        # Publish messages to the "missing_entity_fetched" channel
        redis_eventpublisher.initiate_fetch_missing_data(
            entity=entity, session=session, redis_client=redis_client
        )

        # Wait for messages on the "missing_entity_fetched" channel
        messages_missing_entity = wait_for_messages(pubsub_missing_entity, timeout=3)

        # Handle messages on the "missing_entity_fetched" channel
        for message in messages_missing_entity:
            redis_eventconsumer_missing_entity_fetched.handle_message(message=message)

        # Wait for messages on the "updated_entity_prepared" channel
        messages_updated_entity = wait_for_messages(pubsub_updated_entity, timeout=3)

        for message in messages_updated_entity:
            redis_eventconsumer_update_data_prepared.handle_message(
                message=message, session=session
            )

        # Assert
        rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 220})
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
        session.execute(text("DELETE FROM party_style"))
        session.execute(text("DELETE FROM party"))
