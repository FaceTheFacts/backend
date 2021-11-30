# std
from typing import Optional, List

# third-party
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate

# local
import src.api.crud as crud
import src.api.schemas as schemas
from src.db import models
from src.db.connection import Session
from src.api.utils.error import check_entity_not_found

app = FastAPI()


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# CORS-policy
# * docs: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Cache-Control"] = "no-store"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js 'sha256-R2r7jpC1j6BEeer9P/YDRn6ufsaSnnARhKTdfrSKStk='; style-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css; frame-ancestors 'none'"

    # HTML-related (future-proof)
    response.headers["Feature-Policy"] = "'none'"
    response.headers["Referrer-Policy"] = "no-referrer"

    return response


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/politician/{id}", response_model=schemas.Politician)
def read_politician(
    id: int,
    db: Session = Depends(get_db),
    sidejobs_start: int = None,
    sidejobs_end: int = None,
    votes_start: int = None,
    votes_end: int = 5,
):
    politician = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(politician, "Politician")

    sidejobs = crud.get_sidejobs_by_politician_id(db, id)[sidejobs_start:sidejobs_end]
    politician.__dict__["sidejobs"] = sidejobs

    votes_and_polls = crud.get_votes_and_polls_by_politician_id(
        db, id, (votes_start, votes_end)
    )
    politician.__dict__["votes_and_polls"] = votes_and_polls

    return politician


@app.get("/top-candidates", response_model=List[schemas.PoliticianSearch])
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


@app.get(
    "/politician/{id}/constituencies", response_model=schemas.PoliticianToConstituencies
)
def read_politician_constituencies(id: int, db: Session = Depends(get_db)):
    politician = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(politician, "Politician")
    return politician


@app.get("/politician/{id}/positions", response_model=schemas.PoliticianToPosition)
def read_politician_positions(id: int, db: Session = Depends(get_db)):
    politician = crud.get_entity_by_id(db, models.Politician, id)
    check_entity_not_found(politician, "Politician")
    return politician


@app.get("/politician/{id}/sidejobs", response_model=Page[schemas.Sidejob])
def read_politician_sidejobs(id: int, db: Session = Depends(get_db)):
    sidejobs = crud.get_sidejobs_by_politician_id(db, id)
    return paginate(sidejobs)


@app.get("/search", response_model=Page[schemas.PoliticianSearch])
def read_politician_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_search(db, text)
    check_entity_not_found(politicians, "Politicians")
    return paginate(politicians)


@app.get("/image-scanner", response_model=Page[schemas.PoliticianSearch])
def read_politician_image_scanner(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_image_scanner(db, text)
    check_entity_not_found(politicians, "Politicians")
    return paginate(politicians)


@app.get("/politician/{id}/votes", response_model=Page[schemas.VoteAndPoll])
def read_politician_votes(
    id: int,
    db: Session = Depends(get_db),
    filters: List[int] = Query(None),
):
    votes = crud.get_votes_and_polls_by_politician_id(db, id, (None, None), filters)
    check_entity_not_found(votes, "Votes")
    return paginate(votes)


@app.get("/bundestag-latest-polls", response_model=Page[schemas.BundestagPoll])
def read_latest_polls(db: Session = Depends(get_db)):
    polls = crud.get_polls_total(db)
    check_entity_not_found(polls, "Polls")
    return paginate(polls)


@app.get("/poll/{id}/details", response_model=List[schemas.PollResult])
def read_poll_details(id: int, db: Session = Depends(get_db)):
    poll_results = crud.get_poll_results_by_poll_id(db, id)
    check_entity_not_found(poll_results, "Poll Results")
    return poll_results


# https://uriyyo-fastapi-pagination.netlify.app/
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
