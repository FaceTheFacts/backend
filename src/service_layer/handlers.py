# std
import json
import logging
from typing import Any, List

# local
from src.domain import events, commands
from src.api import repository
from src.entrypoints import redis_eventpublisher
from src.logging_config import configure_logging
from src.service_layer import utils


configure_logging()
logger = logging.getLogger(__name__)


# Step 1
def fetch_missing_entity(command: commands.FetchMissingEntity) -> List[Any]:
    if command.entity == "party":
        repo = repository.SqlAlchemyFactory(command.session).create_party_repository()
        missing_party_data = utils.FetchMissingEntity(
            "parties", repo
        ).fetch_missing_entities()
        return missing_party_data
    
    if command.entity == "parliament":
        repo = repository.SqlAlchemyFactory(command.session).create_parliament_repository()
        missing_parliament_data = utils.FetchMissingEntity(
            "parliaments", repo
        ).fetch_missing_entities()
        return missing_parliament_data
    
    if command.entity == "parliament-period":
        repo = repository.SqlAlchemyFactory(command.session).create_parliament_period_repository()
        missing_parliament_period_data = utils.FetchMissingEntity(
            "parliament-periods", repo
        ).fetch_missing_entities()
        return missing_parliament_period_data
    return []


# Step 2
def prepare_update_data(command: commands.PrepareUpdateData):
    if command.entity == "party":
        party_styles = [
            {
                "id": api_party["id"],
                "display_name": api_party["label"],
                "foreground_color": "#FFFFFF",
                "background_color": "#333333",
                "border_color": None,
            }
            for api_party in command.data
        ]
        parties = [
            {
                "id": api_party["id"],
                "entity_type": api_party["entity_type"],
                "label": api_party["label"],
                "api_url": api_party["api_url"],
                "full_name": api_party["full_name"],
                "short_name": api_party["short_name"],
                "party_style_id": api_party["id"],
            }
            for api_party in command.data
        ]
        # return events.UpdatedEntityPrepared(
        #     entities=["party_style", "party"], data=[party_styles, parties]
        # )
        return {"entities": ["party_style", "party"], "data": [party_styles, parties]}
    
    if command.entity == "parliament":
        parliaments = [
            {
                "id": api_parliament["id"],
                "entity_type": api_parliament["entity_type"],
                "label": api_parliament["label"],
                "api_url": api_parliament["api_url"],
                "abgeordnetenwatch_url": api_parliament["abgeordnetenwatch_url"],
                "label_external_long": api_parliament["label_external_long"],
            }
            for api_parliament in command.data
        ]
        return {"entities": ["parliament"], "data": [parliaments]}
    
    if command.entity == "parliament-period":
        parliament_periods = [
            {
                "id": api_parliament_period["id"],
                "entity_type": api_parliament_period["entity_type"],
                "label": api_parliament_period["label"],
                "api_url": api_parliament_period["api_url"],
                "abgeordnetenwatch_url": api_parliament_period["abgeordnetenwatch_url"],
                "type": api_parliament_period["type"],
                "election_date": api_parliament_period["election_date"],
                "start_date_period": api_parliament_period["start_date_period"],
                "end_date_period": api_parliament_period["end_date_period"],
                "parliament_id": api_parliament_period["parliament"]["id"],
                "previous_period_id": api_parliament_period["previous_period"]["id"] if api_parliament_period["previous_period"] else None,
            }
            for api_parliament_period in command.data
        ]
        return {"entities": ["parliament_period"], "data": [parliament_periods]}


# Step 3
def update_table(command: commands.UpdateTable):
    factory = repository.SqlAlchemyFactory(command.session)
    if command.entities == ["party_style", "party"]:
        party_style_repo = factory.create_party_style_repository()
        party_repo = factory.create_party_repository()
        party_style_repo.add_or_update_list(command.data[0])  # type: ignore
        party_repo.add_or_update_list(command.data[1])  # type: ignore
    
    if command.entities == ["parliament"]:
        parliament_repo = factory.create_parliament_repository()
        parliament_repo.add_or_update_list(command.data[0])
    
    if command.entities == ["parliament_period"]:
        parliament_period_repo = factory.create_parliament_period_repository()
        parliament_period_repo.add_or_update_list(command.data[0])


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
