# std
from typing import Optional

# 3rd-party
from fastapi import FastAPI

# local
from backend import fetch, preprocess


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
