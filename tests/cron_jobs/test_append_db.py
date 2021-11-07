# local
from src.cron_jobs.append_db import append_sidejobs
from src.db.models.sidejob import Sidejob
from src.db.connection import Session
import src.db.models as models

# third-party
from sqlalchemy import delete

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
        assert (
            append_sidejobs()[0]["label"] == "Mitglied des Stiftungsrates, ehrenamtlich"
        )
        assert append_sidejobs()[0]["id"] == 11699

    drop_last_item_and_update()
