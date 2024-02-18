# std
import logging
from typing import Union

# local
from src.domain import control_commands as commands
from src.domain import control_events as events
from src.logging_config import configure_logging
from src.service_layer import control_handlers as handlers

configure_logging()
logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


def handle(message: Message):  # type: ignore
    results = []
    queue = [message]
    while queue:
        event = queue.pop(0)
        if isinstance(event, events.Event):
            handle_event(event, queue)
        elif isinstance(event, commands.Command):
            cmd_result = handle_command(event, queue)
            results.append(cmd_result)
        else:
            raise Exception(f"{event} was not an Event or Command")
    return results


def handle_event(event: events.Event, queue: list[Message]):
    for handler in EVENT_HANDLERS[type(event)]:  # type: ignore
        try:
            logger.info("handling event with handler %s", handler)
            handler(event)
            # queue.extend(collect_new_events(event))

        except Exception:
            logger.exception("Exception handling event with handler %s", handler)
            continue


def handle_command(command: commands.Command, queue: list[Message]):
    # logger.info("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]  # type: ignore
        result = handler(command)
        # queue.extend(collect_new_events(command))
        return result
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS = {
    events.MissingEntityFetched: [handlers.publish_missing_entity_fetched_event],
    events.UpdatedEntityPrepared: [handlers.publish_update_data_prepared_event],
}

COMMAND_HANDLERS = {
    commands.FetchMissingEntity: handlers.fetch_missing_entity,
    commands.PrepareUpdateData: handlers.prepare_update_data,
    commands.UpdateTable: handlers.update_table,
    commands.LoadJsonData: handlers.load_json_data,
}
