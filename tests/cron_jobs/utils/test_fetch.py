# local
from src.cron_jobs.utils.fetch import (
    fetch_entity_count,
    fetch_json,
    fetch_missing_entity,
)
from src.db.models.sidejob import Sidejob

# third party
import pytest


def test_fetch_json():
    def page_not_found():
        with pytest.raises(Exception):
            fetch_json("random_url")

    page_not_found()


def test_fetch_entity_count():
    def page_not_found():
        with pytest.raises(Exception):
            fetch_json("random_url")

    page_not_found()
