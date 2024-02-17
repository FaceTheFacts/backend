# std
import logging
import json
import os

# local
from src.logging_config import configure_logging
from src.domain import control_commands as commands
from src.service_layer import control_messsagebus as messagebus
from src.db.connection import Session

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