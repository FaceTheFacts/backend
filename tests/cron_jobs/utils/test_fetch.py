# std
import requests

# local
from src.cron_jobs.utils.fetch import fetch_entity_count, fetch_json

# third party
import pytest


def test_fetch_json():
    def page_not_found():
        with pytest.raises(Exception):
            fetch_json("random_url")

    def fetch_cities():
        assert fetch_json(
            "https://www.abgeordnetenwatch.de/api/v2/cities?range_end=0"
        ) == {
            "meta": {
                "abgeordnetenwatch_api": {
                    "version": "2.0",
                    "changelog": "https://www.abgeordnetenwatch.de/api/version-changelog/aktuell",
                    "licence": "CC0 1.0",
                    "licence_link": "https://creativecommons.org/publicdomain/zero/1.0/deed.de",
                    "documentation": "https://www.abgeordnetenwatch.de/api/entitaeten/city",
                },
                "status": "ok",
                "status_message": "",
                "result": {"count": 0, "total": 1065, "range_start": 0, "range_end": 0},
            },
            "data": [],
        }

    page_not_found()
    fetch_cities()


# def test_fetch_entity_count():
#     def page_not_found():
#       with pytest.raises(requests.exceptions.RequestException):
#         fetch_entity_count("city")
#     page_not_found()
# assert fetch_entity_count("cities") == 1065
