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


# Step 3
def update_table(command: commands.UpdateTable):
    factory = repository.SqlAlchemyFactory(command.session)
    if command.entities == ["party_style", "party"]:
        party_style_repo = factory.create_party_style_repository()
        party_repo = factory.create_party_repository()
        party_style_repo.add_or_update_list(command.data[0])  # type: ignore
        party_repo.add_or_update_list(command.data[1])  # type: ignore


def publish_missing_entity_fetched_event(
    event: events.MissingEntityFetched,
):
    redis_eventpublisher.publish(
        channel="missing_entity_fetched",
        message=json.dumps({"entity": event.entity, "data": event.data}),
    )


def publish_update_data_prepared_event(
    event: events.UpdatedEntityPrepared,
):
    redis_eventpublisher.publish(
        channel="updated_entity_prepared",
        message=json.dumps(
            {
                "entities": event.entities,
                "data": event.data,
            }
        ),
    )


def send_table_updated_notification(
    event: events.TableUpdated,
):
    logger.info(f"Table updated for {event.entities}")
    print(f"Table updated for {event.entities}")
