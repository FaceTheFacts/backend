# std
from typing import Optional

# 3rd-party
from fastapi import FastAPI

# local
from backend import fetch, preprocess, sort


app = FastAPI()


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/politicians/{id}")
def politician(id: int):
    # fetch data
    data = fetch.politician(id)

    # preprocess attributes
    data["occupation"] = preprocess.occupation(data["occupation"])
    data["party"]["label"] = preprocess.party(data["party"]["label"])

    # return json
    return data


@app.get("/candidacies-mandates/")
def candidacies_mandates(politician_id: int):
    # fetch mandate
    data = fetch.mandate(politician_id)

    # fetch and sort first vote
    first_vote = fetch.first_vote(data["electoral_data"]["constituency"]["id"])
    data["first_vote"] = sort.first_vote(first_vote)

    # fetch and sort second_vote
    second_vote = fetch.second_vote(
        data["electoral_data"]["electoral_list"]["id"], data["party"]["id"]
    )
    data["second_vote"] = sort.second_vote(second_vote)

    # return json
    return data
