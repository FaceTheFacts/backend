# std
from typing import List

# third-party
from sqlalchemy.orm import Session

# local
import src.db.models as models
import src.api.schemas as schemas

# SELECT * FROM Country.__tablename__ WHERE id = id;
def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()


# SELECT * FROM Poll.__tablename__ WHERE id = id;
def get_poll_by_id(db: Session, id: int):
    return db.query(models.Poll).filter(models.Poll.id == id).first()


# SELECT * FROM Politician.__tablename__ WHERE id = id;
def get_politician_by_id(db: Session, id: int):
    return db.query(models.Politician).filter(models.Politician.id == id).first()


# SELECT * FROM Sidejob.__tablename__ WHERE id = id;
def get_sidejob_by_id(db: Session, id: int):
    return db.query(models.Sidejob).filter(models.Sidejob.id == id).first()


# SELECT id FROM CandidacyMandate.__tablename__ WHERE politician_id == id;
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


# SELECT id FROM CandidacyMandate.__tablename__ WHERE politician_id == id;
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


# sidejob_ids = SELECT id FROM CandidacyMandate.__tablename__ WHERE politician_id == id;
# for sidejob_id in sidejob_ids:
#     SELECT * FROM Sidejob.__tablename__ WHERE id = sidejob_id;
def get_sidejobs_by_politician_id(db: Session, id: int) -> List[schemas.Sidejob]:
    data_list = []
    sidejob_ids = get_sidejob_ids_by_politician_id(db, id)
    for sidejob_id in sidejob_ids:
        sidejob = get_sidejob_by_id(db, sidejob_id)
        data_list.append(sidejob)
    return data_list


# SELECT * FROM Politician.__tablename__ WHERE label LIKE %{partial_name}%;
def get_politicians_by_partial_name(db: Session, partial_name: str):
    return (
        db.query(models.Politician)
        .where(models.Politician.label.ilike(f"%{partial_name}%"))
        .all()
    )


# constituency_id = SELECT constituency_id FROM ZipCode.__tablename__ WHERE zip_code = zipcode;
def get_politicians_by_zipcode(db: Session, zipcode: int):
    constituency_id = (
        db.query(models.ZipCode.constituency_id)
        .filter(models.ZipCode.zip_code == str(zipcode))
        .first()["constituency_id"]
    )

    if constituency_id is None:
        return []
    # electoral_data_ids = SELECT id FROM ElectoralData.__tablename__ WHERE constituency_id = constituency_id;
    electoral_data_ids = (
        db.query(models.ElectoralData.id)
        .filter(models.ElectoralData.constituency_id == constituency_id)
        .all()
    )
    # for electoral_data_id in electoral_data_ids:
    #     politician_ids = SELECT politician_id FROM CandidacyMandate.__tablename__ WHERE electoral_data_id = electoral_data_id.id
    politician_ids = []
    for electoral_data_id in electoral_data_ids:
        politician_ids.append(
            db.query(models.CandidacyMandate.politician_id)
            .filter(models.CandidacyMandate.electoral_data_id == electoral_data_id.id)
            .first()
        )
    # for politician_id in politician_ids:
    #     SELECT * FROM Politician.__tablename__ WHERE id = politician_id.politician_id
    politicians = []
    for politician_id in politician_ids:
        politicians.append(
            db.query(models.Politician)
            .filter(models.Politician.id == politician_id.politician_id)
            .first()
        )

    return politicians


# try:
#     SELECT constituency_id FROM ZipCode.__tablename__ WHERE zip_code = search_text;
# except ValueError:
#     SELECT * FROM Politician.__tablename__ WHERE label LIKE %{partial_name}%;
def get_politician_by_search(db: Session, search_text: str):
    try:
        zipcode = int(search_text)
        return get_politicians_by_zipcode(db, zipcode)
    except ValueError:
        return get_politicians_by_partial_name(db, search_text)
