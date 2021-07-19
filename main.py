# std
from typing import List, Optional

# 3rd-party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local
from backend import fetch, preprocess
from backend.types import ComitteeMembership, Mandate, Politician, Poll, Sidejob, Vote


app = FastAPI()

# CORS-policy
# * docs: https://fastapi.tiangolo.com/tutorial/cors/
# * TODO: Can we restrict this policy? E.g. https-only
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/candidacies-mandates/", response_model=Mandate)
def candidacies_mandates(politician_id: int):
    # fetch mandate
    data = fetch.mandate(politician_id)

    # fetch and preprocess first vote
    first_vote = fetch.first_vote(
        data["electoral_data"]["constituency"]["id"], data["parliament_period"]["id"]
    )
    data["first_vote"] = preprocess.first_vote(first_vote)

    # fetch and preprocess second_vote
    second_vote = fetch.second_vote(
        data["electoral_data"]["electoral_list"]["id"], data["party"]["id"]
    )
    data["second_vote"] = preprocess.second_vote(second_vote)

    data["electoral_data"]["electoral_list"]["label"] = preprocess.constituency(data["electoral_data"]["electoral_list"]["label"])

    data["party"]["label"] = preprocess.party(data["party"]["label"])

    # return json
    return data


@app.get("/committee-memberships", response_model=ComitteeMembership)
def committee_memberships(politician_name: str):
    return fetch.committee_memberships(politician_name)


@app.get(
    "/politicians",
    summary="Search politicians by name",
    response_model=List[Politician],
)
def politicians_search(name: str):
    # fetch data
    politicians = fetch.politicians_search(name)

    # preprocess attributes for each politician
    for p in politicians:
        p["image"] = fetch.image(p["id"])
        p["party"]["label"] = preprocess.party(p["party"]["label"])

    return politicians


@app.get("/politicians/{id}", summary="Politician profile", response_model=Politician)
def politicians(id: int):
    # fetch data
    data = fetch.politician(id)
    data["image"] = fetch.image(id)

    # preprocess attributes
    data["occupation"] = preprocess.occupation(data["occupation"], id)
    data["party"]["label"] = preprocess.party(data["party"]["label"])

    # return json
    return data


@app.get("/politicians/{id}/image", response_model=Optional[str])
def politician_image(id: int):
    return fetch.image(id)


@app.get("/polls/{id}", response_model=Poll)
def polls(id: str):
    return fetch.poll(id)


@app.get("/sidejobs", response_model=List[Sidejob])
def sidejobs(politician_name: str):
    return fetch.sidejobs(politician_name)


@app.get("/votes", response_model=Vote)
def votes(vote_id: str, politician_name: str):
    return fetch.vote(vote_id, politician_name)
