# local
from src.cron_jobs.append_db import append_sidejobs
from src.db.connection import Session
import src.db.models as models

# third-party
from sqlalchemy import delete
from unittest import TestCase

session = Session()


def drop_last_item(model):
    last_id = session.query(model).order_by(model.id.desc()).first().id
    stmt = delete(model).where(model.id == last_id)
    session.execute(stmt)
    session.commit()
    session.close()


def test_append_sidejobs():
    def drop_last_item_and_update():
        drop_last_item(models.Sidejob)
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

    drop_last_item_and_update()
    fetch_nothing()


# def test_append_polls():
#     def drop_last_item_and_update():
#         last_id = (
#             session.query(models.Poll).order_by(models.Poll.id.desc()).first().id
#         )
#         stmt = delete(models.Poll).where(models.Poll.id == last_id)
#         session.execute(stmt)
#         session.commit()
#         session.close()
