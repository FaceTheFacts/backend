# std
import os
from typing import List
from datetime import timedelta

# third-party
import requests
from jose import jwt, JWTError
from fastapi import Depends, Response, Query, APIRouter, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.security import OAuth2PasswordRequestForm

# local
import src.api.crud as crud
import src.api.schemas as schemas
from src.api.utils import politrack
from src.api.utils.politician import get_politician_profile
from src.api.utils.oauth2bearer import OAuth2PasswordBearerWithCookie
from src.db import models
from src.api.security import create_access_token
from src.db.connection import Session
from src.api.utils.error import check_entity_not_found
from src.api.utils.party_sort import party_sort
from src.api.utils.polls import get_politcian_ids_by_bundestag_polldata_and_follow_ids
from src.api.hashing import Hasher

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


def authenticate_user(username: str, password: str, db: Session):
    print(username)
    user = crud.get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(
        minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


@router.get("/politician/{id}", response_model=schemas.Politician)
def read_politician(
    id: int,
    db: Session = Depends(get_db),
    votes_start: int = None,
    votes_end: int = 6,
):
    return get_politician_profile(id, db, votes_start, votes_end)


@router.get("/politicians/", response_model=List[schemas.Politician])
def read_politicians(
    ids: List[int] = Query(None),
    db: Session = Depends(get_db),
    votes_start: int = None,
    votes_end: int = 6,
):
    politicians = [None] * len(ids)
    list_index = 0
    for id in ids:
        politician = get_politician_profile(id, db, votes_start, votes_end)
        politicians[list_index] = politician
        list_index += 1
    return politicians


@router.get("/politicianshistory/", response_model=List[schemas.PoliticianHeader])
def read_politicians(
    ids: List[int] = Query(None),
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
    "/politician/{id}/constituencies", response_model=schemas.ConstituencyPoliticians
)
def read_politician_constituencies(id: int, db: Session = Depends(get_db)):
    constituency_politicians = crud.get_politician_by_constituency(db, id)
    check_entity_not_found(constituency_politicians, "ConstituencyPolitician")
    return constituency_politicians


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


@router.get("/search", response_model=List[schemas.PoliticianHeader])
def read_politician_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_search(db, text)
    check_entity_not_found(politicians, "Politicians")
    sorted_politicians = party_sort(politicians)
    return sorted_politicians


@router.get("/image-scanner", response_model=List[schemas.PoliticianHeader])
def read_politician_image_scanner(id: int, db: Session = Depends(get_db)):
    politician = crud.get_politicians_by_ids(db, [id])
    check_entity_not_found(politician, "Politicians")
    return politician


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


@router.get("/poll/{id}/details", response_model=schemas.PollDetails)
def read_poll_details(id: int, db: Session = Depends(get_db)):
    poll_results = crud.get_poll_results_by_poll_id(db, id)
    poll_links = crud.get_poll_links_by_poll_id(db, id)
    poll_details = {"poll_results": poll_results, "poll_links": poll_links}
    check_entity_not_found(poll_details, "PollDetails")
    return poll_details


@router.get("/poll/{id}/votes", response_model=schemas.PollVotes)
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
def read_politician_speech(id: int, page: int):
    politician_speech = crud.get_politician_speech(id, page)
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
def read_bundestag_speech(page: int, db: Session = Depends(get_db)):
    politician_speech = crud.get_bundestag_speech(db, page)
    check_entity_not_found(politician_speech, "Politician Speech")
    return politician_speech


@router.get("/bundestag/sidejobs", response_model=List[schemas.SidejobBundestag])
def read_politician_sidejobs(db: Session = Depends(get_db)):
    sidejobs = crud.get_latest_sidejobs(db)
    check_entity_not_found(sidejobs, "Sidejobs")
    return sidejobs


@router.get("/bundestag/allsidejobs", response_model=Page[schemas.SidejobBundestag])
def read_politician_sidejobs(db: Session = Depends(get_db)):
    sidejobs = crud.get_all_sidejobs(db)
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
