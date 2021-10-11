# std
from typing import List, Optional

# 3rd-party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local
from connection import Session

app = FastAPI()
db = Session()
# CORS-policy
# * docs: https://fastapi.tiangolo.com/tutorial/cors/
# * TODO: Can we restrict this policy? E.g. https-only
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}

