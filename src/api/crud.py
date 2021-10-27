# std
from typing import List

# 3rd-party
from sqlalchemy.orm import Session

# local
import src.db.models as models
import src.api.schemas as schemas


def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()


def get_poll_by_id(db: Session, id: int):
    return db.query(models.Poll).filter(models.Poll.id == id).first()


def get_politician_by_id(db: Session, id: int):
    return db.query(models.Politician).filter(models.Politician.id == id).first()


def get_sidejob_by_id(db: Session, id: int):
    return db.query(models.Sidejob).filter(models.Sidejob.id == id).first()


def get_candidacy_mandate_ids_by_politician_id(db: Session, id: int) -> List[int]:
    data_list = []
    data = (
        db.query(models.CandidacyMandate.id)
        .filter(models.CandidacyMandate.politician_id == id)
        .all()
    )
    for datum in data:
        data_list.append(datum["id"])
    return data_list


def get_sidejob_ids_by_politician_id(db: Session, id: int) -> List[int]:
    data_list = []
    candidacy_mandate_ids = get_candidacy_mandate_ids_by_politician_id(db, id)
    for candidacy_mandate_id in candidacy_mandate_ids:
        data = db.query(models.SidejobHasMandate.sidejob_id).filter(
            models.SidejobHasMandate.candidacy_mandate_id == candidacy_mandate_id
        )
        for datum in data:
            if datum != None:
                data_list.append(datum["sidejob_id"])

    return data_list


def get_sidejobs_by_politician_id(db: Session, id: int) -> List[schemas.Sidejob]:
    data_list = []
    sidejob_ids = get_sidejob_ids_by_politician_id(db, id)
    for sidejob_id in sidejob_ids:
        sidejob = get_sidejob_by_id(db, sidejob_id)
        data_list.append(sidejob)
    return data_list