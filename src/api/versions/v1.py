# std
import os
from typing import List

# third-party
import requests
from fastapi import Depends, Query, APIRouter, HTTPException, Path
from fastapi_pagination import Page, add_pagination, paginate

# local
import src.api.crud as crud
from src.api.repository import SqlAlchemyFactory
import src.api.schemas as schemas
from src.api.utils import politrack
from src.api.utils.politician import get_politician_profile
from src.db import models
from src.db.connection import Session
from src.api.utils.error import check_entity_not_found
from src.api.utils.party_sort import party_sort
from src.api.utils.polls import get_politcian_ids_by_bundestag_polldata_and_follow_ids
from src.redis_cache.cache import ONE_DAY_IN_SECONDS, ONE_YEAR_IN_SECONDS, custom_cache

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


@router.get(
    "/politician/{id}",
    response_model=schemas.Politician,
    summary="Get detailed information about a specific politician",
    description="Returns detailed information about a politician based on the provided ID, including their party, occupations, side jobs, CVs, and voting records",
)
def read_politician(
    id: int = Path(
        ..., description="The ID of the politician to retrieve", example=79137
    ),
    db: Session = Depends(get_db),
    votes_start: int = Query(None, description="Starting index of votes", example=0),
    votes_end: int = Query(6, description="Ending index of votes", example=6),
):
    return get_politician_profile(id, db, votes_start, votes_end)


@router.get(
    "/politicians/",
    response_model=List[schemas.Politician],
    summary="Get detailed information about a list of politicians",
    description="Returns detailed information about a list of politicians based on the provided list of IDs, including their party, occupations, side jobs, CVs, and voting records",
)
def read_politicians(
    ids: List[int] = Query(
        None, description="A list of politician IDs to retrieve", example=[79137, 66924]
    ),
    db: Session = Depends(get_db),
    votes_start: int = Query(None, description="Starting index of votes", example=0),
    votes_end: int = Query(6, description="Ending index of votes", example=6),
):
    politicians = [None] * len(ids)
    list_index = 0
    for id in ids:
        politician = get_politician_profile(id, db, votes_start, votes_end)
        politicians[list_index] = politician
        list_index += 1
    return politicians


@router.get(
    "/politicianshistory/",
    response_model=List[schemas.PoliticianHeader],
    summary="Get a list of politicians by their IDs",
    description="Returns a list of politicians with basic information (ID, name, and party) based on the provided list of IDs",
)
def read_politicians(
    ids: List[int] = Query(
        None, description="A list of politician IDs to retrieve basic information for"
    ),
    db: Session = Depends(get_db),
):
    politicians = [None] * len(ids)
    list_index = 0
    for id in ids:
        politician = crud.get_entity_by_id(db, models.Politician, id)
        politicians[list_index] = politician
        list_index += 1
    return politicians


@router.get(
    "/politician/{id}/constituencies",
    response_model=schemas.ConstituencyPoliticians,
    summary="Get the constituency and politicians associated with a specific politician",
    description="Returns the constituency and a list of politicians representing the same constituency as the politician with the provided ID",
)
def read_politician_constituencies(id: int, db: Session = Depends(get_db)):
    constituency_politicians = crud.get_politician_by_constituency(db, id)
    check_entity_not_found(constituency_politicians, "ConstituencyPolitician")
    return constituency_politicians


@router.get(
    "/politician/{id}/positions",
    response_model=schemas.PoliticianToPosition,
    summary="Get the poisitions associated with a specific politician",
    description="Returns a list of positions associated with the politician with the provided ID",
)
def read_politician_positions(id: int, db: Session = Depends(get_db)):
    positions = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(positions, "Position")
    return positions


# Tested with mockup
@router.get(
    "/politician/{id}/sidejobs",
    response_model=Page[schemas.Sidejob],
    summary="Get the sidejobs associated with a specific politician",
    description="Returns a list of sidejobs associated with the politician with the provided ID",
)
def read_politician_sidejobs(id: int, db: Session = Depends(get_db)):
    sidejobs = crud.get_sidejobs_by_politician_id(db, id, "v1")
    check_entity_not_found(sidejobs, "Sidejobs")
    return paginate(sidejobs)


@router.get(
    "/search",
    response_model=List[schemas.PoliticianHeader],
    summary="Get the Politicans associated with a specific search term",
    description="Returns a list of Politicans associated with the search term",
)
def read_politician_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_search(db, text)
    check_entity_not_found(politicians, "Politicians")
    sorted_politicians = party_sort(politicians)
    return sorted_politicians


@router.get(
    "/search-zipcode",
    response_model=List[schemas.PoliticianHeader],
    summary="Get the Politicans associated with a specific zip code",
    description="Returns a list of Politicans associated with the zip code",
)
def read_politician_zipcode_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politicians_by_zipcode(db, text)
    check_entity_not_found(politicians, "Politicians")
    sorted_politicians = party_sort(politicians)
    return sorted_politicians


@router.get(
    "/search-name",
    response_model=List[schemas.PoliticianHeader],
    summary="Get the Politicians associated with a specific search term",
    description="Returns a list of Politicians associated with the search term",
)
def read_politician_name_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politicians_by_partial_name(db, text)
    check_entity_not_found(politicians, "Politicians")
    sorted_politicians = party_sort(politicians)
    return sorted_politicians


@router.get("/image-scanner", response_model=List[schemas.PoliticianHeader])
def read_politician_image_scanner(id: int, db: Session = Depends(get_db)):
    politician = crud.get_politicians_by_ids(db, [id])
    check_entity_not_found(politician, "Politicians")
    return politician


@router.get(
    "/politician/{id}/votes",
    response_model=Page[schemas.VoteAndPoll],
    summary="Get the Polls and Votes associated with a specific politician",
    description="Returns a list of Polls and Votes associated with the politician with the provided ID",
)
def read_politician_votes(
    id: int,
    db: Session = Depends(get_db),
    filters: List[int] = Query(None),
):
    votes = crud.get_votes_and_polls_by_politician_id(db, id, (None, None), filters)
    check_entity_not_found(votes, "Votes")
    return paginate(votes)


# Tested with mockup


@router.get(
    "/poll/{id}/details",
    response_model=schemas.PollDetails,
    summary="Get more detailed information about the Poll asssociated with a specific ID",
    description="Returns detailed information about a Poll associated with the provided ID",
)
def read_poll_details(id: int, db: Session = Depends(get_db)):
    poll_results = crud.get_poll_results_by_poll_id(db, id)
    poll_links = crud.get_poll_links_by_poll_id(db, id)
    poll_details = {"poll_results": poll_results, "poll_links": poll_links}
    check_entity_not_found(poll_details, "PollDetails")
    return poll_details


@router.get(
    "/poll/{id}/votes",
    response_model=schemas.PollVotes,
    summary="Get the votes associated with the specific ID",
    description="Returns the yes, no, abstain and no show votes as a List of politicians associate with the specific ID",
)
def read_poll_votes(id: int, db: Session = Depends(get_db)):
    vote_results = crud.get_votes_by_poll_id(db, id)
    check_entity_not_found(vote_results, "Poll Results")
    return vote_results


@router.get("/polls/{id}", response_model=List[schemas.VoteAndPoll])
def read_polls(
    id: int, db: Session = Depends(get_db), filters: List[int] = Query(None)
):
    polls = crud.get_votes_and_polls_by_politician_id(db, id, (None, None), filters)
    check_entity_not_found(polls, "Polls")
    return polls


@router.get("/politician/{id}/speeches", response_model=schemas.PoliticianSpeechData)
@custom_cache(expire=ONE_DAY_IN_SECONDS, ignore_args=["db"])
async def read_politician_speech(id: int, page: int = 1, db: Session = Depends(get_db)):
    politician_speech = crud.get_politician_speech(db, id, page)
    if not politician_speech:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "size": 0,
            "is_last_page": True,
            "politician_id": id,
        }
    return politician_speech


@router.get("/bundestag/speeches", response_model=schemas.ParliamentSpeechData)
@custom_cache(expire=ONE_DAY_IN_SECONDS * 6, ignore_args=["db"])
async def read_bundestag_speech(page: int = 1, db: Session = Depends(get_db)):
    politician_speech = crud.get_bundestag_speech(db, page)
    check_entity_not_found(politician_speech, "Politician Speech")
    return politician_speech


@router.get("/bundestag/sidejobs", response_model=List[schemas.SidejobBundestag])
def read_politician_sidejobs(db: Session = Depends(get_db)):
    sidejobs = crud.get_latest_sidejobs(db, "v1")
    check_entity_not_found(sidejobs, "Sidejobs")
    return sidejobs


@router.get("/bundestag/allsidejobs", response_model=Page[schemas.SidejobBundestag])
def read_politician_sidejobs(db: Session = Depends(get_db)):
    sidejobs = crud.get_all_sidejobs(db, "v1")
    check_entity_not_found(sidejobs, "Sidejobs")
    return paginate(sidejobs)


@router.get(
    "/bundestag/polls", response_model=List[schemas.BundestagPollDataWithPoliticians]
)
def read_latest_polls(
    follow_ids: List[int] = Query(None), db: Session = Depends(get_db)
):
    polls = crud.get_polls_total(db)
    latest_polls = get_politcian_ids_by_bundestag_polldata_and_follow_ids(
        polls, db, follow_ids
    )
    check_entity_not_found(latest_polls, "Polls")
    return latest_polls


@router.get("/bundestag/allpolls", response_model=schemas.BundestagPoll)
def read_latest_polls(
    filters: List[int] = Query(None),
    db: Session = Depends(get_db),
    page: int = Query(1),
):
    size = page * 10
    filtered_polls = crud.get_all_polls_total(db, size, filters)
    polls = {}
    polls["data"] = get_politcian_ids_by_bundestag_polldata_and_follow_ids(
        filtered_polls, db
    )
    if len(polls["data"]) < 10:
        polls["last_page"] = True
    else:
        polls["last_page"] = False
    check_entity_not_found(polls, "Polls")
    return polls


@router.get("/politician/{id}/news", response_model=Page[schemas.PolitrackNewsArticle])
@custom_cache(expire=ONE_YEAR_IN_SECONDS)
async def read_politician_news(id: int):
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


@router.get(
    "/homepagepartydonations", response_model=List[schemas.HomepagePartyDonation]
)
def read_homepage_party_donations(db: Session = Depends(get_db)):
    bundestag_party_ids = [1, 2, 3, 4, 5, 8, 9, 145]
    party_donations = crud.get_homepage_party_donations(db, bundestag_party_ids)

    return party_donations


@router.get("/partydonations", response_model=List[schemas.PartyDonation])
def read_party_donations(db: Session = Depends(get_db)):
    factory = SqlAlchemyFactory(db)
    repo = factory.create_party_donation_repository()
    party_donations = repo.list()
    check_entity_not_found(party_donations, "Party Donations")
    return party_donations
