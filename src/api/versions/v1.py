# std
import os
from typing import List

# third-party
import requests
from fastapi import Depends, Query, APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

# local
import src.api.crud as crud
import src.api.schemas as schemas
from src.api.utils import politrack
from src.api.utils.politician import get_politician_info
from src.db import models
from src.db.connection import Session
from src.api.utils.error import check_entity_not_found

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={404: {"description": "v1 Not found"}},
)


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@router.get("/politician/{id}", response_model=schemas.Politician)
def read_politician(
    id: int,
    db: Session = Depends(get_db),
    sidejobs_start: int = None,
    sidejobs_end: int = None,
    votes_start: int = None,
    votes_end: int = 5,
):
    return get_politician_info(
        id, db, sidejobs_start, sidejobs_end, votes_start, votes_end
    )


@router.get("/politicians/", response_model=List[schemas.Politician])
def read_politicians(
    ids: List[int] = Query(None),
    db: Session = Depends(get_db),
    sidejobs_start: int = None,
    sidejobs_end: int = None,
    votes_start: int = None,
    votes_end: int = 5,
):
    politicians = [None] * len(ids)
    list_index = 0
    for id in ids:
        politician = get_politician_info(
            id, db, sidejobs_start, sidejobs_end, votes_start, votes_end
        )
        politicians[list_index] = politician
        list_index += 1
    return politicians


@router.get("/top-candidates", response_model=List[schemas.PoliticianSearch])
def read_top_candidates(db: Session = Depends(get_db)):
    top_candidates_ids = [
        "130072",
        "79475",
        "66924",
        "119742",
        "145755",
        "108379",
        "135302",
        "79454",
    ]
    politicians = crud.get_politicians_by_ids(db, top_candidates_ids)
    check_entity_not_found(politicians, "Politicians")
    return politicians


@router.get(
    "/politician/{id}/constituencies", response_model=schemas.PoliticianToConstituencies
)
def read_politician_constituencies(id: int, db: Session = Depends(get_db)):
    politician = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(politician, "Politician")
    return politician


@router.get("/politician/{id}/positions", response_model=schemas.PoliticianToPosition)
def read_politician_positions(id: int, db: Session = Depends(get_db)):
    positions = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(positions, "Position")
    return positions


# Tested with mockup
@router.get("/politician/{id}/sidejobs", response_model=Page[schemas.Sidejob])
def read_politician_sidejobs(id: int, db: Session = Depends(get_db)):
    sidejobs = crud.get_sidejobs_by_politician_id(db, id)
    check_entity_not_found(sidejobs, "Sidejobs")
    return paginate(sidejobs)


@router.get("/search", response_model=List[schemas.PoliticianSearch])
def read_politician_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_search(db, text)
    check_entity_not_found(politicians, "Politicians")
    return politicians


@router.get("/image-scanner", response_model=List[schemas.PoliticianSearch])
def read_politician_image_scanner(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_image_scanner(db, text)
    check_entity_not_found(politicians, "Politicians")
    return politicians


@router.get("/politician/{id}/votes", response_model=Page[schemas.VoteAndPoll])
def read_politician_votes(
    id: int,
    db: Session = Depends(get_db),
    filters: List[int] = Query(None),
):
    votes = crud.get_votes_and_polls_by_politician_id(db, id, (None, None), filters)
    check_entity_not_found(votes, "Votes")
    return paginate(votes)


# Tested with mockup
@router.get("/bundestag-latest-polls", response_model=Page[schemas.BundestagPoll])
def read_latest_polls(db: Session = Depends(get_db)):
    polls = crud.get_polls_total(db)
    check_entity_not_found(polls, "Polls")
    return paginate(polls)


@router.get("/poll/{id}/details", response_model=List[schemas.PollResult])
def read_poll_details(id: int, db: Session = Depends(get_db)):
    poll_results = crud.get_poll_results_by_poll_id(db, id)
    check_entity_not_found(poll_results, "Poll Results")
    return poll_results


@router.get("/politician/{id}/speeches", response_model=schemas.PoliticianSpeechData)
def read_politician_speech(id: int, page: int):
    politician_speech = crud.get_politician_speech(id, page)
    check_entity_not_found(politician_speech, "Politician Speech")
    return politician_speech


@router.get("/politician/{id}/news", response_model=Page[schemas.PolitrackNewsArticle])
def read_politician_news(id: int):
    header = politrack.generate_authenticated_header()
    response = requests.get(
        os.environ["POLITRACK_API_URL"] + f"/v1/articles/{id}", headers=header
    )
    if response.status_code == 200:
        articles = response.json()["articles"]
        check_entity_not_found(articles, "Politrack News Articles")
        return paginate(articles)
    else:
        detail = "Unknown External API Error"
        if response.text:
            detail = response.text
        raise HTTPException(status_code=response.status_code, detail=detail)


# https://uriyyo-fastapi-pagination.netlify.app/
add_pagination(router)
