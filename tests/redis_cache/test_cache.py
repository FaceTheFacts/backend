# tests/test_cache.py
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.redis_cache.cache import custom_cache

app = FastAPI()


@app.get("/test_custom_cache/{item_id}")
@custom_cache(expire=5, ignore_args=["request"])
async def custom_cache_route(item_id: int):
    data = {"id": item_id, "message": "Hello, FastAPI Redis Cache!"}
    return data


client = TestClient(app)


def test_custom_cache_response():
    response = client.get("/test_custom_cache/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Hello, FastAPI Redis Cache!"}

    # Cache should be working, the same result should be retrieved without calling the function again
    response = client.get("/test_custom_cache/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Hello, FastAPI Redis Cache!"}

    # Since the cache has an expiration of 5 seconds, we wait for 6 seconds to ensure the cache expires
    import time

    time.sleep(6)

    response = client.get("/test_custom_cache/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "message": "Hello, FastAPI Redis Cache!"}
