from sqlalchemy.orm import Session

import models


def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()
