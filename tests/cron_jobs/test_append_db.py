# local
from src.cron_jobs.append_db import append_polls, append_sidejobs, append_votes
from src.db.connection import Session
import src.db.models as models

# third-party
from sqlalchemy import delete
from unittest import TestCase

session = Session()


def return_last_id(model: any):
    return session.query(model).order_by(model.id.desc()).first().id


def delete_last_item(last_id, model: any, column: str):
    stmt = delete(model).where(model.__dict__[column] == last_id)
    session.execute(stmt)
    session.commit()
    session.close()


def test_append_sidejobs():
    def delete_last_item_and_update():
        last_id = return_last_id(models.Sidejob)
        delete_last_item(last_id, models.Sidejob, "id")
        expected_dict = {
            "additional_information": None,
            "api_url": "https://www.abgeordnetenwatch.de/api/v2/sidejobs/11699",
            "category": "29230",
            "created": 1635272113,
            "data_change_date": "2021-10-26",
            "entity_type": "sidejob",
            "field_city_id": 65,
            "field_country_id": 61,
            "id": 11699,
            "income_level": None,
            "interval": None,
            "job_title_extra": None,
            "label": "Mitglied des Stiftungsrates, ehrenamtlich",
            "sidejob_organization_id": 1107,
        }
        TestCase().assertDictEqual(expected_dict, append_sidejobs()[0])

    def fetch_nothing():
        assert append_sidejobs() == print("Nothing fetched")

    delete_last_item_and_update()
    fetch_nothing()


def test_append_polls():
    def delete_last_item_and_update():
        last_id = return_last_id(models.Poll)
        delete_last_item(last_id, models.PollHasTopic, "poll_id")
        delete_last_item(last_id, models.Poll, "id")

        expected = "https://www.abgeordnetenwatch.de/api/v2/polls/4363"
        assert append_polls()[0]["api_url"] == expected

    def fetch_nothing():
        assert append_polls() == print("Nothing fetched")

    delete_last_item_and_update()
    fetch_nothing()


def test_append_votes():
    def delete_last_item_and_update():
        last_id = return_last_id(models.Vote)
        delete_last_item(last_id, models.Vote, "id")

        assert append_votes()[0]["api_url"] == ""

    delete_last_item_and_update()
