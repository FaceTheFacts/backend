# std
import json
import time
from sqlalchemy import text

# third-party
from tenacity import Retrying, RetryError, stop_after_delay

# local
from src.entrypoints import (
    redis_utils,
    redis_eventpublisher,
    redis_eventconsumer_missing_entity_fetched,
    redis_eventconsumer_update_data_prepared,
)
from src.db.models.party import Party


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

        # messages = []
        # for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        #     with attempt:
        #         message = pubsub.get_message(timeout=1)
        #         if message:
        #             messages.append(message)
        #             print(message)
        #         data = json.loads(messages[-1]["data"])
        #         assert data["entity"] == entity

        # if message:
        #     messages.append(message)
        #     data = json.loads(messages[-1]["data"])
        #     assert data == ""
        # assert data["entities"] == ["party_style", "party"]
        # assert data["data"] == 2

        #         redis_eventconsumer_missing_entity_fetched.handle_message(
        #             message=message_from_channel_one
        #         )
        #         message_from_channel_two = pubsub.get_message(timeout=1)
        #         assert message_from_channel_two ==[]
        #         messages.append(message_from_channel_two)
        #         if message_from_channel_two:
        #             redis_eventconsumer_update_data_prepared.handle_message(
        #                 message=message_from_channel_two, session=session
        #             )
        # return messages
        # Assert
        # assert messages == []
        # data = json.loads(messages[-1]["data"])
        # assert data["entities"] == [entity, "party_style"]
        # assert len(data["data"]) == 2
        # rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 8})
        # assert list(rows) == [""]

    # def test_update_party_related_table_with_mock_data(self, session):
    #     redis_client = RedisClient(host="localhost", port=6379)
    #     pubsub = redis_client.pubsub()
    #     pubsub.subscribe("updated_entity_prepared")
    #     # Arrange
    #     entities = ["party_style", "party"]
    #     data = [
    #         [
    #             {
    #                 "id": 1,
    #                 "display_name": "SPD",
    #                 "foreground_color": "#000000",
    #                 "background_color": "#FFFFFF",
    #                 "border_color": "#000000",
    #             },
    #             {
    #                 "id": 2,
    #                 "display_name": "SPD",
    #                 "foreground_color": "#000000",
    #                 "background_color": "#FFFFFF",
    #                 "border_color": "#000000",
    #             },
    #         ],
    #         [
    #             {
    #                 "id": 1,
    #                 "entity_type": "party",
    #                 "label": "SPD",
    #                 "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
    #                 "full_name": "Sozialdemokratische Partei Deutschlands",
    #                 "short_name": "SPD",
    #                 "party_style_id": 1,
    #             },
    #             {
    #                 "id": 2,
    #                 "entity_type": "party",
    #                 "label": "CDU",
    #                 "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
    #                 "full_name": "Christlich Demokratische Union Deutschlands",
    #                 "short_name": "CDU",
    #                 "party_style_id": 2,
    #             },
    #         ],
    #     ]
    #     # Act
    #     redis_client.publish(
    #         channel="updated_entity_prepared",
    #         message=json.dumps({"entities": entities, "data": data}),
    #     )
    #     # Assert
    #     messages = []
    #     for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
    #         with attempt:
    #             message = pubsub.get_message(timeout=1)
    #             if message:
    #                 messages.append(message)
    #                 print(message)
    #             data = json.loads(messages[-1]["data"])
    #             assert data["entities"] == ["party_style", "party"]
    #             assert len(data["data"]) == 2
