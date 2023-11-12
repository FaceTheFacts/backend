# std
import logging

# local
from src.domain import events
from src.service_layer import handlers


def handle(event: events.Event):  # type: ignore
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:  # type: ignore
            try:
                results.append(handler(event))
            except Exception:
                logging.exception("Exception handling %s", event)
                raise
    return results


HANDLERS = {
    events.MissingEntityFetched: [handlers.prepare_update_data],
    events.UpdatedEntityPrepared: [handlers.update_table],
}
