from typing import Any, TypedDict
import requests


class ApiResponse(TypedDict):
    meta: dict[str, Any]
    data: list[Any]


def request(url: str) -> ApiResponse:
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as err:
        raise Exception(err)
