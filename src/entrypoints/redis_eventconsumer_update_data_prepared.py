# std
import logging
import json
import os

# local
from src.logging_config import configure_logging
from src.domain import commands
from src.service_layer import messagebus
from src.db.connection import Session
from src.entrypoints.redis_utils import RedisClient

# third-party
import redis

configure_logging()
logger = logging.getLogger(__name__)

session = Session()


def handle_message(message, session):
    try:
        data = json.loads(message["data"])
        if message["channel"] == "updated_entity_prepared":
            cmd = commands.UpdateTable(
                entities=data["entities"], data=data["data"], session=session
            )
            messagebus.handle(cmd)
            logger.info("Updated database with with tables: %s", data["entities"])
            logger.info("Executed UpdateTable command")
    except Exception as e:
        logger.exception("Exception executing command: %s", e)


def main():
    """Run the Redis event consumer."""
    logger.info("Running the Redis event consumer")
    pubsub = RedisClient().pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("updated_entity_prepared")
    for message in pubsub.listen():
        handle_message(message, session=session)


if __name__ == "__main__":
    main()
