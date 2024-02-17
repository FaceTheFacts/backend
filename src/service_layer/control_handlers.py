# std
import json
import logging
from typing import Any, List

# local
from src.domain import control_commands as commands
from src.domain import control_events as events
from src.api import repository
from src.service_layer import control_utils as utils

logger = logging.getLogger(__name__)


# Step 1
def fetch_missing_entity(command: commands.FetchMissingEntity) -> List[Any]:
    if command.entity == "vote":
        repo = repository.SqlAlchemyFactory(command.session).create_vote_repository()
        missing_vote_data = utils.FetchMissingEntity(
            "votes", repo
        ).fetch_missing_entities()
        return missing_vote_data
    if command.entity == "party":
        repo = repository.SqlAlchemyFactory(command.session).create_party_repository()
        missing_party_data = utils.FetchMissingEntity(
            "parties", repo
        ).fetch_missing_entities()
        return missing_party_data

    if command.entity == "politician":
        repo = repository.SqlAlchemyFactory(
            command.session
        ).create_politician_repository()
        missing_politician_data = utils.FetchMissingEntity(
            "politicians", repo
        ).fetch_missing_entities()
        return missing_politician_data

    return []


# Step 2
def prepare_update_data(command: commands.PrepareUpdateData):
    if command.entity == "vote":
        return {"entities": ["vote"], "data": utils.prepare_vote_data(command.data)}
    elif command.entity == "party":
        party_styles, parties = utils.prepare_party_data(command.data)
        return {"entities": ["party_style", "party"], "data": [party_styles, parties]}
    elif command.entity == "politician":
        return {
            "entities": ["politician"],
            "data": utils.prepare_politician_data(command.data),
        }


# Step 3
def update_table(command: commands.UpdateTable):
    factory = repository.SqlAlchemyFactory(command.session)

    if command.entities == ["vote"]:
        vote_repo = factory.create_vote_repository()
        vote_repo.add_or_update_list(command.data[0])

    if command.entities == ["party_style", "party"]:
        party_style_repo = factory.create_party_style_repository()
        party_repo = factory.create_party_repository()
        party_style_repo.add_or_update_list(command.data[0])  # type: ignore
        party_repo.add_or_update_list(command.data[1])  # type: ignore

    if command.entities == ["politician"]:
        politician_repo = factory.create_politician_repository()
        politician_repo.add_or_update_list(command.data[0])


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
