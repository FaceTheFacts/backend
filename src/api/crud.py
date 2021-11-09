# std
import urllib.request
from urllib.error import HTTPError
from typing import List

# third-party
from sqlalchemy.orm import Session

# local
import src.db.models as models
import src.api.schemas as schemas
from src.api.utils.sidejob import convert_income_level


def get_country_by_id(db: Session, id: int):
    return db.query(models.Country).filter(models.Country.id == id).first()


def get_politician_by_id(db: Session, id: int):
    return db.query(models.Politician).filter(models.Politician.id == id).first()


def get_politicians_by_ids(db: Session, ids: list):
    politicians = []
    for id in ids:
        politicians.append(get_politician_by_id(db, id))
    return add_image_urls_to_politicians(politicians)


def get_votes_and_polls_by_politician_id(
    db: Session, politician_id: int, range_of_votes: tuple
):
    candidacy_mandate_ids = get_candidacy_mandate_ids_by_politician_id(
        db, politician_id
    )

    votes = (
        db.query(models.Vote, models.Poll)
        .filter(models.Vote.mandate_id.in_(candidacy_mandate_ids))
        .filter(models.Vote.poll_id == models.Poll.id)
        .filter(models.Vote.vote != "no_show")
        .order_by(models.Poll.field_poll_date.desc())[
            range_of_votes[0] : range_of_votes[1]
        ]
    )

    return votes


def get_sidejob_by_id(db: Session, id: int):
    sidejob = db.query(models.Sidejob).filter(models.Sidejob.id == id).first()
    sidejob.income_level = convert_income_level(sidejob.income_level)
    return sidejob


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


def get_politicians_by_partial_name(db: Session, partial_name: str):
    return (
        db.query(models.Politician)
        .where(models.Politician.label.ilike(f"%{partial_name}%"))
        .all()
    )


def get_politicians_by_zipcode(db: Session, zipcode: int):

    politicians = (
        db.query(models.Politician)
        .filter(models.ZipCode.zip_code == str(zipcode))
        .filter(models.ElectoralData.constituency_id == models.ZipCode.constituency_id)
        .filter(models.CandidacyMandate.electoral_data_id == models.ElectoralData.id)
        .filter(models.Politician.id == models.CandidacyMandate.politician_id)
        .all()
    )

    return politicians


def get_politician_by_search(db: Session, search_text: str):
    try:
        zipcode = int(search_text)
        politicians = get_politicians_by_zipcode(db, zipcode)
    except ValueError:
        politicians = get_politicians_by_partial_name(db, search_text)

    return add_image_urls_to_politicians(politicians)


def get_politician_by_image_scanner(db: Session, search_text: str):
    politicians = get_politicians_by_partial_name(db, search_text)
    return add_image_urls_to_politicians(politicians)


def add_image_urls_to_politicians(politicians: list):
    for politician in politicians:
        image_url = (
            "https://candidate-images.s3.eu-central-1.amazonaws.com/{}.jpg".format(
                politician.id
            )
        )

        try:
            urllib.request.urlopen(image_url)
            politician.__dict__["image_url"] = image_url
        except HTTPError:
            politician.__dict__["image_url"] = None

    return politicians
