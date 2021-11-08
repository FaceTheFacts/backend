# std
from typing import Optional, List

# third-party
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate

# local
import src.api.crud as crud
import src.api.schemas as schemas
from src.db.connection import Session

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
# * TODO: Can we restrict this policy? E.g. https-only
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/poll/{id}", response_model=schemas.Poll)
def read_poll(id: int, db: Session = Depends(get_db)):
    poll = crud.get_poll_by_id(db, id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll


@app.get("/politician/{id}")
def read_politician(
    id: int,
    db: Session = Depends(get_db),
    sidejobs_start: int = None,
    sidejobs_end: int = None,
    votes_start: int = None,
    votes_end: int = 5,
):
    politician = crud.get_politician_by_id(db, id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")

    sidejobs = crud.get_sidejobs_by_politician_id(db, id)[sidejobs_start:sidejobs_end]
    politician.__dict__["sidejobs"] = sidejobs

    votes_and_polls = crud.get_votes_and_polls_by_politician_id(
        db, id, (votes_start, votes_end)
    )
    politician.__dict__["votes_and_polls"] = votes_and_polls

    return politician


@app.get(
    "/politician/{id}/constituencies", response_model=schemas.PoliticianToConstituencies
)
def read_politician_constituencies(id: int, db: Session = Depends(get_db)):
    politician = crud.get_politician_by_id(db, id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")
    return politician


@app.get("/politician/{id}/positions", response_model=schemas.PoliticianToPosition)
def read_politician_positions(id: int, db: Session = Depends(get_db)):
    politician = crud.get_politician_by_id(db, id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")
    return politician


@app.get("/politician/{id}/sidejobs", response_model=Page[schemas.Sidejob])
def read_politician_sidejobs(id: int, db: Session = Depends(get_db)):
    sidejobs = crud.get_sidejobs_by_politician_id(db, id)
    return paginate(sidejobs)


@app.get("/search", response_model=Page[schemas.PoliticianSearch])
def read_politician_search(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_search(db, text)
    if politicians is None:
        raise HTTPException(status_code=404, detail="Politicians not found")
    return paginate(politicians)


@app.get("/image-scanner", response_model=Page[schemas.PoliticianSearch])
def read_politician_image_scanner(text: str, db: Session = Depends(get_db)):
    politicians = crud.get_politician_by_image_scanner(db, text)
    if politicians is None:
        raise HTTPException(status_code=404, detail="Politicians not found")
    return paginate(politicians)


# https://uriyyo-fastapi-pagination.netlify.app/
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
