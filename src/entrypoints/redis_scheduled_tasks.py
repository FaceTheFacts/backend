import time
import threading
from src.entrypoints import (
    redis_utils,
    redis_eventconsumer_missing_entity_fetched,
    redis_eventconsumer_update_data_prepared,
    redis_eventpublisher,
)
from src.db.connection import Session

redis_client = redis_utils.RedisClient()
session = Session()

# Caution: This task needs multiple threads to run.


def subscribe_missing_entity_fetched():
    """Subscribe to missing_entity_fetched."""
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("missing_entity_fetched")

    start_time = time.time()
    duration = 120

    while time.time() - start_time <= duration:
        message = pubsub.get_message(timeout=1)
        if message:
            redis_eventconsumer_missing_entity_fetched.handle_message(message)

    print(
        "subscribe_missing_entity_fetched: Duration of {} seconds has passed".format(
            duration
        )
    )


def subscribe_updated_entity_prepared():
    """Subscribe to updated_entity_prepared."""
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

    print(
        "subscribe_updated_entity_prepared: Duration of {} seconds has passed".format(
            duration
        )
    )


def publish_entity():
    """Run the Redis event publisher."""
    redis_eventpublisher.initiate_fetch_missing_data(
        entity="party", session=session, redis_client=redis_client
    )


if __name__ == "__main__":
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
