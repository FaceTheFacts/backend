# std
import logging
from typing import Any

# local
from src.domain import control_commands as commands
from src.domain import control_events as events
from src.entrypoints.redis_utils import RedisClient
from src.logging_config import configure_logging
from src.service_layer import control_messsagebus as messagebus
from src.db.connection import Session

configure_logging()
logger = logging.getLogger(__name__)

session = Session()


def initiate_fetch_missing_data(entity: str, session: Any, redis_client=RedisClient()):
    try:
        # Step 1: Execute FetchMissingEntity command
        fetch_command = commands.FetchMissingEntity(entity=entity, session=session)
        missing_data = messagebus.handle(fetch_command)
        # publish a message
        event = events.MissingEntityFetched(
            entity=entity, data=missing_data[0], redis_client=redis_client
        )
        messagebus.handle(event)
        logger.info("Total missing data: %s", len(missing_data[0]))
        logger.info("Executed FetchMissingEntity command")

    except Exception as e:
        logger.exception("Exception executing command: %s", e)