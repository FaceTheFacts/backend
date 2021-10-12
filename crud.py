from sqlalchemy.orm import Session

import models


def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()

def get_poll_by_id(db: Session, id: int):
    return db.query(models.Poll).filter(models.Poll.id == id).first()

def get_committee_by_id(db: Session, id: int):
    return db.query(models.Committee).filter(models.Committee.id == id).first()
