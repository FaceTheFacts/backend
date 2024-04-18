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


# Step 1
def fetch_missing_entity(command: commands.FetchMissingEntity) -> List[Any]:
    repo = None
    if command.entity == Entity.PARTY.value:
        repo = repository.SqlAlchemyFactory(command.session).create_party_repository()
    elif command.entity == Entity.PARLIAMENT.value:
        repo = repository.SqlAlchemyFactory(
            command.session
        ).create_parliament_repository()
    elif command.entity == Entity.PARLIAMENT_PERIOD.value:
        repo = repository.SqlAlchemyFactory(
            command.session
        ).create_parliament_period_repository()
    elif command.entity == Entity.TOPIC.value:
        repo = repository.SqlAlchemyFactory(command.session).create_topic_repository()
    elif command.entity == Entity.COMMITTEE.value:
        repo = repository.SqlAlchemyFactory(
            command.session
        ).create_committee_repository()
    elif command.entity == Entity.POLL.value:
        repo = repository.SqlAlchemyFactory(command.session).create_poll_repository()

    if repo is not None:
        missing_entity_data = utils.FetchMissingEntity(
            command.entity, repo
        ).fetch_missing_entities()
        return missing_entity_data
    return []


# Step 2
def prepare_update_data(command: commands.PrepareUpdateData):
    if command.entity == Entity.PARTY.value:
        party_styles, parties = utils.prepare_party_data(command.data)
        return {
            "entities": [Entity.PARTY_STYLE.value, Entity.PARTY.value],
            "data": [party_styles, parties],
        }
    elif command.entity == Entity.PARLIAMENT.value:
        parliaments = utils.prepare_parliament_data(command.data)
        return {"entities": [Entity.PARLIAMENT.value], "data": [parliaments]}
    elif command.entity == Entity.PARLIAMENT_PERIOD.value:
        parliament_periods = utils.prepare_parliament_period_data(command.data)
        return {
            "entities": [Entity.PARLIAMENT_PERIOD.value],
            "data": [parliament_periods],
        }
    elif command.entity == Entity.TOPIC.value:
        topics = utils.prepare_topic_data(command.data)
        return {"entities": [Entity.TOPIC.value], "data": [topics]}
    elif command.entity == Entity.COMMITTEE.value:
        committees = utils.prepare_committee_data(command.data)
        committee_has_topics = utils.prepare_committee_has_topic_data(command.data)
        return {
            "entities": [Entity.COMMITTEE.value, Entity.COMMITTEE_HAS_TOPIC.value],
            "data": [committees, committee_has_topics],
        }
    elif command.entity == Entity.POLL.value:
        polls = utils.prepare_poll_data(command.data)
        return {"entities": [Entity.POLL.value], "data": [polls]}

    else:
        return {"entities": [], "data": []}


# Step 3
def update_table(command: commands.UpdateTable):
    factory = repository.SqlAlchemyFactory(command.session)

    for entity in command.entities:
        if entity == Entity.PARTY_STYLE.value:
            party_style_repo = factory.create_party_style_repository()
            party_style_repo.add_or_update_list(command.data[0])
        elif entity == Entity.PARTY.value:
            party_repo = factory.create_party_repository()
            party_repo.add_or_update_list(command.data[1])
        elif entity == Entity.PARLIAMENT.value:
            parliament_repo = factory.create_parliament_repository()
            parliament_repo.add_or_update_list(command.data[0])
        elif entity == Entity.PARLIAMENT_PERIOD.value:
            parliament_period_repo = factory.create_parliament_period_repository()
            parliament_period_repo.add_or_update_list(command.data[0])
        elif entity == Entity.TOPIC.value:
            topic_repo = factory.create_topic_repository()
            topic_repo.add_or_update_list(command.data[0])
        elif entity == Entity.COMMITTEE.value:
            committee_repo = factory.create_committee_repository()
            committee_repo.add_or_update_list(command.data[0])
        elif entity == Entity.COMMITTEE_HAS_TOPIC.value:
            committee_has_topic_repo = factory.create_committee_has_topic_repository()
            committee_has_topic_repo.add_or_update_list(command.data[1])
        elif entity == Entity.POLL.value:
            poll_repo = factory.create_poll_repository()
            poll_repo.add_or_update_list(command.data[0])

        else:
            raise ValueError(f"Unknown entity: {entity}")


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
