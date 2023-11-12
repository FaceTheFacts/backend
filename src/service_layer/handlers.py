# std
import logging

# local
from src.domain import events
from src.api import repository


# Step 2
def prepare_update_data(
    event: events.MissingEntityFetched,
):
    if event.entity == "party":
        party_styles = [
            {
                "id": api_party["id"],
                "display_name": api_party["label"],
                "foreground_color": "#FFFFFF",
                "background_color": "#333333",
                "border_color": None,
            }
            for api_party in event.data
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
            for api_party in event.data
        ]
        # return events.UpdatedEntityPrepared(
        #     entities=["party_style", "party"], data=[party_styles, parties]
        # )
        return {"entities": ["party_style", "party"], "data": [party_styles, parties]}


# Step 3
def update_table(
    event: events.UpdatedEntityPrepared
):
    factory = repository.SqlAlchemyFactory(event.session)
    if event.entities == ["party_style", "party"]:
        party_style_repo = factory.create_party_style_repository()
        party_repo = factory.create_party_repository()
        party_style_repo.add_or_update_list(event.data[0])  # type: ignore
        party_repo.add_or_update_list(event.data[1])  # type: ignore
