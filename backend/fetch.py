# std
from typing import Any, Dict

# 3rd-party
import requests


def fetch(url: str, params: Dict[str, Any] = {}):
    BASE_URL = "https://abgeordnetenwatch.de/api/v2"
    return requests.get(f"{BASE_URL}/{url}", params).json()["data"]


# ---


def politician(id: int) -> Dict[str, Any]:
    return fetch(f"politicians/{id}")
