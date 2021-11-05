# std
from typing import Any, TypedDict
import requests
import time
import math


# local
from src.cron_jobs.utils.file import read_json, write_json, has_valid_file
from src.db.connection import Session
from src.db.models.sidejob import Sidejob


PAGE_SIZE = 999


class ApiResponse(TypedDict):
    meta: dict[str, Any]
    data: list[Any]


def fetch_json(url: str) -> ApiResponse:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        raise Exception(err)
    return response.json()


def fetch_page(entity: str, page_nr: int) -> list[Any]:
    url = f"https://www.abgeordnetenwatch.de/api/v2/{entity}?range_start={page_nr * PAGE_SIZE}&range_end={PAGE_SIZE}"
    result: ApiResponse = fetch_json(url)
    return result["data"]


def fetch_entity(entity: str) -> list[Any]:
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
    total_entity = fetch_entity_count(entity)
    session = Session()
    database_rows = session.query(model).count()
    diff = total_entity - database_rows
    if diff:
        print(("You need to fetch {} data").format(diff))
    else:
        print("Table already updated")


def load_entity(entity: str) -> list[Any]:
    file_path = f"src/cron_jobs/data/{entity}.json"
    has_file = has_valid_file(file_path)
    if not has_file:
        data = fetch_entity(entity)
        write_json(file_path, data)
        return data

    data: list[Any] = read_json(file_path)
    return data


if __name__ == "__main__":
    print(fetch_missing_entity("sidejobs", Sidejob))
