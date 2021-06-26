# std
from typing import Optional

# 3rd-party
from fastapi import FastAPI
import requests

# local
from backend import preprocess


# cfg variables
BASE_URL = "https://abgeordnetenwatch.de/api/v2"


app = FastAPI()


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/politicians/{id}")
def politician(id: int):
    # fetch data
    data = requests.get(f"{BASE_URL}/politicians/{id}").json()["data"]

    # preprocess attributes
    data["occupation"] = preprocess.occupation(data["occupation"])
    data["party"]["label"] = preprocess.party(data["party"]["label"])

    # return json
    return data
