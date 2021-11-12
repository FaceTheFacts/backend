# std
from typing import Any, TypedDict, Dict, List
import requests


class ApiResponse(TypedDict):
    meta: Dict[str, Any]
    data: List[Any]


def request(url: str) -> ApiResponse:
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as err:
        raise Exception(err)
