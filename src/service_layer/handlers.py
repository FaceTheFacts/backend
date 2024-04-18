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

    if repo is not None:
        missing_entity_data = utils.FetchMissingEntity(
            command.entity, repo
        ).fetch_missing_entities()
        return missing_entity_data
    return []

    # if command.entity == Entity.PARTY:
    #     repo = repository.SqlAlchemyFactory(command.session).create_party_repository()
    #     missing_party_data = utils.FetchMissingEntity(
    #         Entity.PARTY, repo
    #     ).fetch_missing_entities()
    #     return missing_party_data

    # if command.entity == Entity.PARLIAMENT:
    #     repo = repository.SqlAlchemyFactory(
    #         command.session
    #     ).create_parliament_repository()
    #     missing_parliament_data = utils.FetchMissingEntity(
    #         Entity.PARLIAMENT, repo
    #     ).fetch_missing_entities()
    #     return missing_parliament_data

    # if command.entity == "parliament-period":
    #     repo = repository.SqlAlchemyFactory(
    #         command.session
    #     ).create_parliament_period_repository()
    #     missing_parliament_period_data = utils.FetchMissingEntity(
    #         "parliament-periods", repo
    #     ).fetch_missing_entities()
    #     return missing_parliament_period_data
    # if command.entity == "topic":
    #     repo = repository.SqlAlchemyFactory(command.session).create_topic_repository()
    #     missing_topic_data = utils.FetchMissingEntity(
    #         "topics", repo
    #     ).fetch_missing_entities()
    #     return missing_topic_data
    # if command.entity == "committee":
    #     repo = repository.SqlAlchemyFactory(
    #         command.session
    #     ).create_committee_repository()
    #     missing_committee_data = utils.FetchMissingEntity(
    #         "committees", repo
    #     ).fetch_missing_entities()
    #     return missing_committee_data
    # if command.entity == "poll":
    #     repo = repository.SqlAlchemyFactory(command.session).create_poll_repository()
    #     missing_poll_data = utils.FetchMissingEntity(
    #         "polls", repo
    #     ).fetch_missing_entities()
    #     return missing_poll_data
    # return []


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

    else:
        return {"entities": [], "data": []}
    # if command.entity == "parliament-period":
    #     parliament_periods = utils.prepare_parliament_period_data(command.data)
    #     return {"entities": ["parliament_period"], "data": [parliament_periods]}
    # if command.entity == "topic":
    #     topics = utils.prepare_topic_data(command.data)
    #     return {"entities": ["topic"], "data": [topics]}
    # if command.entity == "committee":
    #     committees = utils.prepare_committee_data(command.data)
    #     committee_has_topics = utils.prepare_committee_has_topic_data(command.data)
    #     return {"entities": ["committee"], "data": [committees, committee_has_topics]}
    # if command.entity == "poll":
    #     polls = utils.prepare_poll_data(command.data)
    #     return {"entities": ["poll"], "data": [polls]}


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

        else:
            raise ValueError(f"Unknown entity: {entity}")

    # if command.entities == ["parliament_period"]:
    #     parliament_period_repo = factory.create_parliament_period_repository()
    #     parliament_period_repo.add_or_update_list(command.data[0])
    # if command.entities == ["topic"]:
    #     topic_repo = factory.create_topic_repository()
    #     topic_repo.add_or_update_list(command.data[0])
    # if command.entities == ["committee"]:
    #     committee_repo = factory.create_committee_repository()
    #     committee_repo.add_or_update_list(command.data[0])
    #     committee_has_topic_repo = factory.create_committee_has_topic_repository()
    #     committee_has_topic_repo.add_or_update_list(command.data[1])
    # if command.entities == ["poll"]:
    #     poll_repo = factory.create_poll_repository()
    #     poll_repo.add_or_update_list(command.data[0])
    #     # add poll has topic
    #     # add poll has field_link


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
