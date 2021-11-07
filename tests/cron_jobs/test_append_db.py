# local
from src.cron_jobs.append_db import append_sidejobs
from src.db.models.sidejob import Sidejob
from src.db.connection import Session
import src.db.models as models

# third-party
from sqlalchemy import delete
from unittest import TestCase

session = Session()


def test_append_sidejobs():
    def drop_last_item_and_update():
        last_id = (
            session.query(models.Sidejob).order_by(models.Sidejob.id.desc()).first().id
        )
        stmt = delete(Sidejob).where(Sidejob.id == last_id)
        session.execute(stmt)
        session.commit()
        session.close()
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
