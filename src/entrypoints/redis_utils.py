# local
import os
from typing import Any
import logging

# third-party
import redis

# local
from src.logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client."""

    def __init__(
        self,
        host: str = os.getenv("REDIS_HOST", "localhost"),
        port: int = int(os.getenv("REDIS_PORT", 6379)),
    ):
        self.host = host
        self.port = port
        self.redis_client = redis.StrictRedis(
            host=self.host, port=self.port, decode_responses=True
        )

    def pubsub(self, ignore_subscribe_messages=True):
        return self.redis_client.pubsub(
            ignore_subscribe_messages=ignore_subscribe_messages
        )

    def publish(self, channel: str, message: Any):
        """Publish a message to a Redis channel."""
        logging.debug("Publishing message to channel %s: %s", channel, message)
        self.redis_client.publish(channel=channel, message=message)
