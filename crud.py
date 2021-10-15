from sqlalchemy.orm import Session

import models


def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()


def get_poll_by_id(db: Session, id: int):
    return db.query(models.Poll).filter(models.Poll.id == id).first()


def get_politician_by_id(db: Session, id: int):
    return db.query(models.Politician).filter(models.Politician.id == id).first()


def get_candidacy_mandate_ids_by_politician_id(db: Session, id: int):
    data_list = []
    data =db.query(models.Candidacy_mandate.id).filter(models.Candidacy_mandate.politician_id == id).all()
    for datum in data:
        data_list.append(datum["id"])
    return data_list


def get_sidejob_ids_by_candidacy_mandate_ids(db: Session, id: int):
    data_list = []
    candidacy_mandate_ids = get_candidacy_mandate_ids_by_politician_id(db, id)
    for candidacy_mandate_id in candidacy_mandate_ids:
        data =db.query(models.SidejobHasMandate.sidejob_id).filter(models.SidejobHasMandate.candidacy_mandate_id == candidacy_mandate_id).slice(0,10)
        for datum in data:
            if datum!=None:
                data_list.append(datum["sidejob_id"])

    return data_list

def get_sidejob_by_id(db: Session, id: int):
    return db.query(models.Sidejob).filter(models.Sidejob.id == id).first()
