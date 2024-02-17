import logging
import json

from src.logging_config import configure_logging
from src.domain import control_commands as commands
from src.domain import control_events as events
from src.entrypoints.redis_utils import RedisClient
from src.service_layer import control_messsagebus as messagebus


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
