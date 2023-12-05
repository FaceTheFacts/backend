# std
import json
import logging
import os
import time
import schedule
from typing import Any

# local
from src.domain import commands, events
from src.logging_config import configure_logging
from src.service_layer import messagebus
from src.db.connection import Session

# third-party
import redis

configure_logging()
logger = logging.getLogger(__name__)

session = Session()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(
    host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True
)

def publish(channel: str, message: Any):
    """Publish a message to a Redis channel."""
    logging.debug("Publishing message to channel %s: %s", channel, message)
    redis_client.publish(channel=channel, message=message)


def initiate_fetch_missing_data(entity: str, session: Any):
    try:
        # Step 1: Execute FetchMissingEntity command
        fetch_command = commands.FetchMissingEntity(entity=entity, session=session)
        missing_data = messagebus.handle(fetch_command)
        # publish a message
        event = events.MissingEntityFetched(entity=entity, data=missing_data[0])
        messagebus.handle(event)
        logger.info("Total missing data: %s", len(missing_data[0]))
        logger.info("Executed FetchMissingEntity command")

    except Exception as e:
        logger.exception("Exception executing command: %s", e)


def main():
    """Run the Redis event publisher."""
    logger.info("Running the Redis event publisher")
    initiate_fetch_missing_data(entity="party", session=session)


if __name__ == "__main__":
    main()

# schedule.every().day.at("02:00").do(
#     initiate_fetch_missing_data, entity="party", session=session
# )

# while True:
#     schedule.run_pending()
#     time.sleep(1)
