# local
from src.cron_jobs.append_db import append_polls, append_sidejobs, append_votes
from src.db.connection import Session
import src.db.models as models
from typing import Any

# third-party
from sqlalchemy import delete
from unittest import TestCase

session = Session()


def return_last_id(model: Any):
    return session.query(model).order_by(model.id.desc()).first().id


def delete_last_item(last_id, model: Any, column: str):
    stmt = delete(model).where(model.__dict__[column] == last_id)
    session.execute(stmt)
    session.commit()
    session.close()


def test_append_sidejobs():
    def delete_last_item_and_update():
        last_id = return_last_id(models.Sidejob)
        delete_last_item(last_id, models.Sidejob, "id")
        
        assert len(append_sidejobs()) >0

    delete_last_item_and_update()


# def test_append_polls():
#     def delete_last_item_and_update():
#         last_id = return_last_id(models.Poll)
#         delete_last_item(last_id, models.PollHasTopic, "poll_id")
#         delete_last_item(last_id, models.Poll, "id")

#         expected = "https://www.abgeordnetenwatch.de/api/v2/polls/4363"
#         assert append_polls()[0]["api_url"] == expected

#     def fetch_nothing():
#         assert append_polls() == print("Nothing fetched")

#     delete_last_item_and_update()
#     fetch_nothing()
