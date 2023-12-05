# std
import logging
import json
import os

# local
from src.logging_config import configure_logging
from src.domain import commands, events
from src.service_layer import messagebus
from src.entrypoints.redis_utils import RedisClient

# third-party
import redis

configure_logging()
logger = logging.getLogger(__name__)


def handle_message(message):
    try:
        data = json.loads(message["data"])
        if message["channel"] == "missing_entity_fetched":
            cmd = commands.PrepareUpdateData(entity=data["entity"], data=data["data"])
            prepared_update_data = messagebus.handle(cmd)
            # Publish a message
            event = events.UpdatedEntityPrepared(
                entities=prepared_update_data[0]["entities"],
                data=prepared_update_data[0]["data"],
                redis_client=RedisClient(),
            )
            messagebus.handle(event)
            logger.info("Executed PrepareUpdateData command")
    except Exception as e:
        logger.exception("Exception executing command: %s", e)


def main():
    """Run the Redis event consumer."""
    logger.info("Running the Redis event consumer")
    pubsub = RedisClient().pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("missing_entity_fetched")
    for message in pubsub.listen():
        handle_message(message)


if __name__ == "__main__":
    main()
