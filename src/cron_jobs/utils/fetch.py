# std
from typing import Any, TypedDict, Dict, List
import requests
import time
import math


# local
from src.cron_jobs.utils.file import read_json, write_json, has_valid_file
from src.db.connection import Session


PAGE_SIZE = 1000


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


def fetch_page(entity: str, page_nr: int) -> List[Any]:
    url = f"https://www.abgeordnetenwatch.de/api/v2/{entity}?range_start={page_nr * PAGE_SIZE}&range_end={PAGE_SIZE}"
    result: ApiResponse = fetch_json(url)
    return result["data"]


def fetch_entity(entity: str) -> List[Any]:
    time_begin = time.time()
    url = f"https://www.abgeordnetenwatch.de/api/v2/{entity}?range_end=0"
    result = fetch_json(url)
    total = result["meta"]["result"]["total"]
    page_count = math.ceil(total / PAGE_SIZE)
    entities = [None] * total
    for page_nr in range(page_count):
        page_entities = fetch_page(entity, page_nr)
        print(f"Page No.{page_nr} of {entity} is fetched")
        for i in range(len(page_entities)):
            entities[i + page_nr * PAGE_SIZE] = page_entities[i]
    print("All data is fetched!")
    time_end = time.time()
    print(f"Total runtime of fetching {entity} is {time_end - time_begin}")
    return entities


def fetch_entity_count(entity: str) -> int:
    url = f"https://www.abgeordnetenwatch.de/api/v2/{entity}?range_end=0"
    result = fetch_json(url)
    total = result["meta"]["result"]["total"]
    return total


def fetch_missing_entity(entity: str, model: Any):
    data_list = []
    total_entity = fetch_entity_count(entity)
    session = Session()
    database_rows: int = session.query(model).count()
    diff = total_entity - database_rows
    # Uncomment line below + Line 86 when you already fetch the data locally
    # file_path = f"src/cron_jobs/data/{entity}.json"
    if diff:
        last_id = session.query(model).order_by(model.id.desc()).first().id
        print(f"The last id of {entity} is: {last_id}")
        result = fetch_json(
            f"https://www.abgeordnetenwatch.de/api/v2/{entity}?id[gt]={last_id}&range_end=0"
        )
        total = result["meta"]["result"]["total"]
        page_count = math.ceil(total / PAGE_SIZE)
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


def fetch_last_id_from_model(model: Any) -> int:
    session = Session()
    last_id = session.query(model).order_by(model.id.desc()).first().id
    return last_id


def fetch_missing_sub_entity(entity: str, model: Any):
    data_list = []
    session = Session()
    # Uncomment line below + Line 86 when you already fetch the data locally
    # file_path = f"src/cron_jobs/data/{entity}.json"
    last_id = session.query(model).order_by(model.id.desc()).first().id
    print(f"The last id of {entity} is: {last_id}")
    result = fetch_json(
        f"https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?{entity}[gt]={last_id}&range_end=0"
    )
    total = result["meta"]["result"]["total"]
    if total:
        page_count = math.ceil(total / PAGE_SIZE)
        for page_num in range(page_count):
            fetched_data = fetch_json(
                f"https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?{entity}[gt]={last_id}&page={page_num}&pager_limit={PAGE_SIZE}"
            )
            data = fetched_data["data"]
            for item in data:
                data_list.append(item)
        print(("Fetched {} data entries").format(len(data_list)))
        return data_list
    else:
        print(f"Table {entity} already updated")


def load_entity(entity: str) -> List[Any]:
    file_path = f"src/cron_jobs/data/{entity}.json"
    has_file = has_valid_file(file_path)
    if not has_file:
        data = fetch_entity(entity)
        write_json(file_path, data)
        return data

    data: List[Any] = read_json(file_path)
    return data


def load_entity_from_db(model: Any) -> List[Any]:
    session = Session()
    ids = session.query(model).order_by(model.id.desc()).all()
    return ids


def check_for_missing_votes_data(model: Any) -> List[Any]:
    file_path = f"src/cron_jobs/data/votes.json"
    data: List[Any] = read_json(file_path)
    session = Session()
    ids = session.query(model).order_by(model.id.desc()).all()
    poll_ids = set([vote.id for vote in ids])
    missing_votes = []
    for vote in data:
        if vote["poll"]["id"] not in poll_ids:
            if vote["poll"]["id"] not in missing_votes:
                missing_votes.append(vote["poll"]["id"])
    write_json("src/cron_jobs/data/missing_votes.json", missing_votes)


def fetch_missing_entity_from_json(entity: str) -> List[Any]:
    file_path = f"src/cron_jobs/data/missing_{entity}.json"
    data: List[Any] = read_json(file_path)
    data_list = []
    for item in data:
        fetched_data = fetch_json(
            f"https://www.abgeordnetenwatch.de/api/v2/{entity}/{item}"
        )
        data = fetched_data["data"]
        data_list.append(data)
    return data_list


def match_constituency_to_parliament_periods(constituency: str) -> int:
    # AW does not include the parliament period in the constituency data so we have to match it manually
    # Change the constutency_map based on the latest data
    constituency_map = {
        "Schleswig-Holstein Wahl 2022": 135,
        "Nordrhein-Westfalen Wahl 2022": 136,
        "Saarland 2022 - 2027": 137,
    }
    for item in constituency_map:
        if item in constituency:
            return constituency_map[item]
