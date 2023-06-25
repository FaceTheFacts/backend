# std
import os
from typing import List

# third-party
import requests
from fastapi import Depends, Query, APIRouter, HTTPException, Path
from fastapi_pagination import Page, add_pagination, paginate

# local
import src.api.crud as crud
import src.api.schemas as schemas
from src.api.utils import politrack
from src.api.utils.politician import did_vote_pass, get_politician_profile
from src.db import models
from src.db.connection import Session
from src.api.utils.error import check_entity_not_found
from src.api.utils.party_sort import party_sort
from src.api.utils.polls import get_politcian_ids_by_bundestag_polldata_and_follow_ids
from src.redis_cache.cache import (
    ONE_DAY_IN_SECONDS,
    ONE_MONTH_IN_SECONDS,
    ONE_WEEK_IN_SECONDS,
    custom_cache,
)

router = APIRouter(
    prefix="/plugin",
    tags=["plugin"],
    responses={404: {"description": "plugin Not found"}},
)

Page_custom = Page.with_custom_options(size=25)

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
    description="Returns detailed information about a politician based on the provided ID, including their party, occupations, side jobs, CVs, committee-membership and voting records",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS)
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
    "/topics/",
    response_model=List[schemas.Topic],
    summary="Get a list of all topics",
    description="Returns a list of all topics, including their IDs, names, and descriptions",
)
@custom_cache(expire=ONE_MONTH_IN_SECONDS)
def read_topics(db: Session = Depends(get_db)):
    return crud.get_topics(db)


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
    response_model=Page_custom[schemas.Sidejob],
    summary="Get the sidejobs associated with a specific politician",
    description="Returns a list of sidejobs associated with the politician with the provided ID",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS, ignore_args=["db"])
def read_politician_sidejobs(id: int, db: Session = Depends(get_db)):
    sidejobs = crud.get_sidejobs_by_politician_id(db, id)
    check_entity_not_found(sidejobs, "Sidejobs")
    return paginate(sidejobs)


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


@router.get(
    "/politician/{id}/votes",
    response_model=Page_custom[schemas.VoteAndPoll],
    summary="Get the Polls and Votes associated with a specific politician",
    description="Returns a list of Polls and Votes associated with the politician with the provided ID and option to filter by topic",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS, ignore_args=["db"])
def read_politician_votes(
    id: int,
    db: Session = Depends(get_db),
    filters: List[int] = Query(None),
):
    votes = crud.get_votes_and_polls_by_politician_id(db, id, (None, None), filters)
    check_entity_not_found(votes, "Votes")
    return paginate(votes)


@router.get(
    "/poll/{id}/details",
    response_model=schemas.PollDetails,
    summary="Get more detailed information about the Poll asssociated with a specific poll ID",
    description="Returns detailed information about voting behaviour of each fraction and links with additional information for a Poll associated with the provided ID",
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
    summary="Get the voting associated with the specific poll ID",
    description="Returns the yes, no, abstain and no show votes as a List of politicians associate with the specific poll ID",
)
def read_poll_votes(id: int, db: Session = Depends(get_db)):
    vote_results = crud.get_votes_by_poll_id(db, id)
    check_entity_not_found(vote_results, "Poll Results")
    return vote_results


@router.get(
    "/politician/{id}/speeches",
    response_model=schemas.PoliticianSpeechData,
    summary="Get the speeches associated with a specific politician ID",
    description="Returns a list of speeches associated with the politician with the provided ID",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS, ignore_args=["db"])
async def read_politician_speech(id: int, page: int = 1, db: Session = Depends(get_db)):
    politician_speech = crud.get_politician_speech(db, id, page, True)
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


@router.get(
    "/bundestag/speeches",
    response_model=schemas.ParliamentSpeechData,
    summary="Get the latest speeches from the parliament",
    description="Returns a list of the latest bundestag speeches including title, date, speaker and link to video",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS, ignore_args=["db"])
async def read_bundestag_speech(page: int = 1, db: Session = Depends(get_db)):
    politician_speech = crud.get_bundestag_speech(db, page, True)
    check_entity_not_found(politician_speech, "Politician Speech")
    return politician_speech


@router.get(
    "/bundestag/sidejobs",
    response_model=Page_custom[schemas.SidejobBundestag],
    summary="Get the latest sidejobs from the parliament",
    description="Returns a list of the latest bundestag sidejobs and the associated politiican",
)
@custom_cache(expire=ONE_WEEK_IN_SECONDS, ignore_args=["db"])
async def read_politician_sidejobs(db: Session = Depends(get_db)):
    sidejobs = crud.get_all_sidejobs(db)
    check_entity_not_found(sidejobs, "Sidejobs")
    return paginate(sidejobs)


@router.get(
    "/bundestag/polls",
    response_model=Page_custom[schemas.PluginPoll],
    summary="Get the latest polls from the parliament",
    description="Returns a list of the latest bundestag polls and the associated result",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS * 3, ignore_args=["db"])
async def read_latest_polls(
    filters: List[int] = Query(None),
    db: Session = Depends(get_db),
):
    polls_with_results = crud.get_bundestag_polls_by_topic(db, filters)
    plugin_polls = [
        schemas.PluginPoll(
            poll=schemas.Poll(
                id=p.id,
                label=p.label,
                field_intro=p.field_intro,
                field_poll_date=p.field_poll_date,
                poll_passed=did_vote_pass(
                    {
                        "yes": p.vote_result.yes,
                        "no": p.vote_result.no,
                        "no_show": p.vote_result.no_show,
                        "abstain": p.vote_result.abstain,
                    }
                ),
            ),
            result=p.vote_result,
        )
        for p in polls_with_results
    ]
    check_entity_not_found(plugin_polls, "PluginPoll")
    return paginate(plugin_polls)


@router.get(
    "/politician/{id}/news",
    response_model=Page_custom[schemas.PolitrackNewsArticle],
    summary="Get the latest news articles associated with a specific politician ID",
    description="Returns a list of news articles associated with the politician with the provided ID",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS * 3)
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


@router.get("/parties", response_model=Page_custom[schemas.Party])
@custom_cache(expire=ONE_WEEK_IN_SECONDS, ignore_args=["db"])
async def get_parties(db: Session = Depends(get_db)):
    parties = crud.get_parties(db)
    check_entity_not_found(parties, "Parties")
    return paginate(parties)


@router.get(
    "/partydonations",
    response_model=Page_custom[schemas.PluginPartyDonation],
    summary="Get the latest party donations",
    description="Returns a list of the latest party donations and the organization with the option to filter after party id",
)
@custom_cache(expire=ONE_DAY_IN_SECONDS * 3, ignore_args=["db"])
async def read_party_donations(
    db: Session = Depends(get_db), filters: List[int] = Query(None)
):
    party_donations = crud.get_all_party_donations(db, filters)
    check_entity_not_found(party_donations, "Party Donations")
    return paginate(party_donations)


# https://uriyyo-fastapi-pagination.netlify.app/
add_pagination(router)

### Buggy routes
""" @router.get(
    "/homepagepartydonations", response_model=List[schemas.HomepagePartyDonation]
)
def read_party_donations(db: Session = Depends(get_db)):
    bundestag_party_ids = [1, 2, 3, 4, 5, 8, 9, 145]
    party_donations = crud.get_homepage_party_donations(db, bundestag_party_ids)

    return party_donations
 """
