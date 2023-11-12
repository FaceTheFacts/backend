# local
from src.domain import events
from src.api import repository
from src.db.connection import Session

# def update_table(
#     event: events.MissingEntityFetched
#     repo: repository
# ):
#     """Update table with data from event"""
#     for entity in event.entity:
#         repo.add_or_update_list(entity)


# TODO
# Implement update_table function
# Implement fetch_missing_entities function
# Combine them with cron job


def update_table(
    event: events.UpdatedEntityPrepared, session: Session()  # type: ignore
):
    factory = repository.SqlAlchemyFactory(session)
    if event.entities == ["party_style", "party"]:
        party_style_repo = factory.create_party_style_repository()
        party_repo = factory.create_party_repository()
        party_style_repo.add_or_update_list(event.data[0])  # type: ignore
        party_repo.add_or_update_list(event.data[1])  # type: ignore
