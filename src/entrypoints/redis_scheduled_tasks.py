# std
import logging
import os
import time
import threading

# third-party
import schedule

# local
from src.entrypoints import (
    redis_utils,
    redis_eventconsumer_missing_entity_fetched,
    redis_eventconsumer_update_data_prepared,
    redis_eventpublisher,
)
from src.db.connection import Session
from src.logging_config import configure_logging


# Caution: This task needs multiple threads to run.
configure_logging()
logger = logging.getLogger(__name__)

redis_client = redis_utils.RedisClient()
session = Session()


def subscribe_missing_entity_fetched():
    """Subscribe to missing_entity_fetched."""
    logger.info("Subscribing to missing_entity_fetched")
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("missing_entity_fetched")

    start_time = time.time()
    duration = 120

    while time.time() - start_time <= duration:
        message = pubsub.get_message(timeout=1)
        if message:
            redis_eventconsumer_missing_entity_fetched.handle_message(message)

    logger.info(
        "subscribe_missing_entity_fetched: Duration of {} seconds has passed".format(
            duration
        )
    )
    logger.info("subscribe_missing_entity_fetched: Stopping")


def subscribe_updated_entity_prepared():
    """Subscribe to updated_entity_prepared."""
    logger.info("subscribe_updated_entity_prepared: Starting")
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("updated_entity_prepared")

    start_time = time.time()
    duration = 120

    while time.time() - start_time <= duration:
        message = pubsub.get_message(timeout=1)
        if message:
            redis_eventconsumer_update_data_prepared.handle_message(
                message, session=session
            )
    logger.info(
        "subscribe_updated_entity_prepared: Duration of {} seconds has passed".format(
            duration
        )
    )
    logger.info("subscribe_updated_entity_prepared: Stopping")


def publish_entity():
    """Run the Redis event publisher."""
    logger.info("Running the Redis event publisher")
    redis_eventpublisher.initiate_load_json(
        entity="party",
        file_path=os.path.join("src", "entrypoints", "example.json"),
        redis_client=redis_client,
    )
    redis_eventpublisher.initiate_fetch_missing_data(
        entity="parliament", session=session, redis_client=redis_client
    )

    redis_eventpublisher.initiate_fetch_missing_data(
        entity="parliament-period", session=session, redis_client=redis_client
    )


def run_tasks():
    # Create threads for each task
    thread_subscribe_missing = threading.Thread(target=subscribe_missing_entity_fetched)
    thread_subscribe_updated = threading.Thread(
        target=subscribe_updated_entity_prepared
    )
    thread_publish = threading.Thread(target=publish_entity)

    # Start the threads
    thread_subscribe_missing.start()
    time.sleep(10)  # Introduce a delay for the second thread
    thread_subscribe_updated.start()
    time.sleep(10)  # Introduce a delay for the third thread
    thread_publish.start()

    # Wait for all threads to finish
    thread_subscribe_missing.join()
    thread_subscribe_updated.join()
    thread_publish.join()


if __name__ == "__main__":
    schedule.every().day.at("16:51").do(run_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)
