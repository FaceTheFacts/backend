# std
import json
import logging
from typing import Any, List

# local
from src.domain import events, commands
from src.api import repository
from src.domain.entities import Entity
from src.logging_config import configure_logging
from src.service_layer import utils


configure_logging()
logger = logging.getLogger(__name__)


ENTITY_HANDLERS = {
    Entity.PARTY.value: utils.prepare_party_data,
    Entity.PARLIAMENT.value: utils.prepare_parliament_data,
    Entity.PARLIAMENT_PERIOD.value: utils.prepare_parliament_period_data,
    Entity.TOPIC.value: utils.prepare_topic_data,
    Entity.COMMITTEE.value: utils.prepare_committee_data,
    Entity.POLL.value: utils.prepare_poll_data,
}

DATA_HANDLERS = {
    Entity.PARTY.value: [Entity.PARTY_STYLE.value, Entity.PARTY.value],
    Entity.PARLIAMENT.value: [Entity.PARLIAMENT.value],
    Entity.PARLIAMENT_PERIOD.value: [Entity.PARLIAMENT_PERIOD.value],
    Entity.TOPIC.value: [Entity.TOPIC.value],
    Entity.COMMITTEE.value: [Entity.COMMITTEE.value, Entity.COMMITTEE_HAS_TOPIC.value],
    Entity.POLL.value: [Entity.POLL.value],
}


# Step 1
def fetch_missing_entity(command: commands.FetchMissingEntity) -> List[Any]:
    repo = utils.get_repository(
        repository.SqlAlchemyFactory(command.session), command.entity
    )

    if repo is not None:
        missing_entity_data = utils.FetchMissingEntity(
            command.entity, repo
        ).fetch_missing_entities()
        return missing_entity_data

    return []


# Step 2
def prepare_update_data(command: commands.PrepareUpdateData):
    entity = command.entity
    data = command.data

    if entity in ENTITY_HANDLERS:
        entity_data = ENTITY_HANDLERS[entity](data)
        return {"entities": DATA_HANDLERS[entity], "data": [entity_data]}
    else:
        return {"entities": [], "data": []}


# Step 3
def update_table(command: commands.UpdateTable):
    factory = repository.SqlAlchemyFactory(command.session)

    for entity, data in zip(command.entities, command.data):
        repo = utils.get_repository(factory, entity)
        if repo is not None:
            repo.add_or_update_list(data)
        else:
            logger.error(f"Repository for entity {entity} not found.")


def publish_missing_entity_fetched_event(
    event: events.MissingEntityFetched,
):
    event.redis_client.publish(
        channel="missing_entity_fetched",
        message=json.dumps({"entity": event.entity, "data": event.data}),
    )


def publish_update_data_prepared_event(
    event: events.UpdatedEntityPrepared,
):
    event.redis_client.publish(
        channel="updated_entity_prepared",
        message=json.dumps(
            {
                "entities": event.entities,
                "data": event.data,
            }
        ),
    )
