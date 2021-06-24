# std
from typing import Optional

# 3rd-party
from fastapi import FastAPI

# local


app = FastAPI()


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}
