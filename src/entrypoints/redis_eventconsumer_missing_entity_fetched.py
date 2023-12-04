# std
import logging
import json
import os

# local
from src.logging_config import configure_logging
from src.domain import commands
from src.service_layer import messagebus

# third-party
import redis

configure_logging()
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(
    host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True
)


def handle_message(message):
    try:
        data = json.loads(message["data"])
        if message["channel"] == "missing_entity_fetched":
            cmd = commands.PrepareUpdateData(entity=data["entity"], data=data["data"])
            prepared_update_data = messagebus.handle(cmd)
            # Publish a message
            redis_client.publish(
                channel="updated_entity_prepared",
                message=json.dumps(
                    {
                        "entities": prepared_update_data[0]["entities"],
                        "data": prepared_update_data[0]["data"],
                    }
                ),
            )
            logger.info("Executed PrepareUpdateData command")
    except Exception as e:
        logger.exception("Exception executing command: %s", e)


def main():
    """Run the Redis event consumer."""
    logger.info("Running the Redis event consumer")
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("missing_entity_fetched")
    for message in pubsub.listen():
        handle_message(message)


if __name__ == "__main__":
    main()
