# std
from typing import List, Optional

# 3rd-party
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# local
import schemas, crud
from database import Session

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


@app.get("/country/{id}", response_model=schemas.Country)
def read_country(id: int, db: Session = Depends(get_db)):
    country = crud.get_country_by_id(db, id)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.get("/poll/{id}", response_model=schemas.Poll)
def read_poll(id: int, db: Session = Depends(get_db)):
    poll = crud.get_poll_by_id(db, id)
    if poll is None:
        raise HTTPException(status_code=404, detail="poll not found")
    return poll
