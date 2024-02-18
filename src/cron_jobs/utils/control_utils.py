import json
from typing import Any, TypedDict, Dict, List
import requests
from src.db.connection import Session
import math
from sqlalchemy.dialects.postgresql import insert

PAGE_SIZE = 1000

entity_list = [
    "politicians",
    "parties",
    "electoral-lists",
    "election-program",
    "polls",
    "candidacies-mandates",
    "committees",
    "committee-memberships",
    "parliaments",
    "parliament-periods",
    "votes",
    "fractions",
    "constituencies",
    "sidejobs",
    "sidejob-organizations",
    "topics",
    "cities",
    "countries",
]


class ApiResponse(TypedDict):
    meta: Dict[str, Any]
    data: List[Any]


def fetch_json(url: str) -> ApiResponse:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        raise Exception(err)
    return response.json()


def fetch_entity_count(entity: str) -> int:
    if entity not in entity_list:
        raise Exception(f"{entity} is not a valid entity")
    url = f"https://www.abgeordnetenwatch.de/api/v2/{entity}?range_end=0"
    result = fetch_json(url)
    total = result["meta"]["result"]["total"]
    return total


def fetch_missing_entity(entity: str, model: Any):
    if entity not in entity_list:
        raise Exception(f"{entity} is not a valid entity")

    total_entity = fetch_entity_count(entity)

    # Start a session to interact with the database
    session = Session()
    try:
        database_rows: int = session.query(model).count()
        diff = total_entity - database_rows

        if diff:
            last_id = session.query(model).order_by(model.id.desc()).first().id
            print(f"The last id of {entity} is: {last_id}")
            # You may also need to handle potential exceptions for network requests here
            result = fetch_json(
                f"https://www.abgeordnetenwatch.de/api/v2/{entity}?id[gt]={last_id}&range_end=0"
            )
            total = result["meta"]["result"]["total"]
            page_count = math.ceil(total / PAGE_SIZE)
            data_list = []
            for page_num in range(page_count):
                fetched_data = fetch_json(
                    f"https://www.abgeordnetenwatch.de/api/v2/{entity}?id[gt]={last_id}&page={page_num}&pager_limit={PAGE_SIZE}"
                )
                data = fetched_data["data"]
                for item in data:
                    data_list.append(item)
            print(("Fetched {} data entries").format(len(data_list)))
            # Uncomment line below when you might have to fetch multiple times from the same entity
            # write_json(file_path, data_list)
            return data_list
        else:
            print(f"Table {entity} already updated")
    finally:
        # Ensure the session is closed after the operation
        session.close()


def fetch_last_id_from_model(model: Any) -> int:
    session = Session()
    try:
        last_id = session.query(model).order_by(model.id.desc()).first().id
        return last_id
    finally:
        session.close()


def load_entity_ids_from_db(model: Any) -> List[Any]:
    session = Session()
    try:
        ids = session.query(model.id).order_by(model.id.desc()).all()
        return [id[0] for id in ids]
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def insert_and_update(model: Any, data: List[Any]) -> None:
    session = Session()
    try:
        stmt = insert(model).values(data)
        stmt = stmt.on_conflict_do_update(
            constraint=f"{model.__tablename__}_pkey",
            set_={col.name: col for col in stmt.excluded if not col.primary_key},
        )
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def load_json_data(entity: str, dir: str):
    try:
        with open(f"{dir}/{entity}.json") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        print("File not found: %s", e)
        return []
