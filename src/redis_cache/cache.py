import asyncio
import os
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import wraps
from http import HTTPStatus
from typing import Dict, Union

from redis import asyncio as aioredis
from fastapi import Response, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from fastapi_redis_cache import FastApiRedisCache
from fastapi_redis_cache.enums import RedisEvent
from fastapi_redis_cache.util import deserialize_json

from src.db.models.politician import Politician


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")
redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
DATETIME_AWARE = "%m/%d/%Y %I:%M:%S %p %z"
DATE_ONLY = "%m/%d/%Y"

ONE_HOUR_IN_SECONDS = 3600
ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24
ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7
ONE_MONTH_IN_SECONDS = ONE_DAY_IN_SECONDS * 30
ONE_YEAR_IN_SECONDS = ONE_DAY_IN_SECONDS * 365


async def get_redis_pool():
    return await aioredis.from_url(redis_url)


async def get_redis(redis_pool: aioredis.Redis = Depends(get_redis_pool)):
    return redis_pool


class CustomFastApiRedisCache(FastApiRedisCache):
    def add_to_cache(self, key: str, value: Dict, expire: int) -> bool:
        response_data = None
        try:
            response_data = BetterJsonEncoder().encode(value)
        except TypeError:
            message = f"Object of type {type(value)} is not JSON-serializable"
            self.log(RedisEvent.FAILED_TO_CACHE_KEY, msg=message, key=key)
            return False
        cached = self.redis.set(name=key, value=response_data, ex=expire)
        if cached:
            self.log(RedisEvent.KEY_ADDED_TO_CACHE, key=key)
        else:
            self.log(RedisEvent.FAILED_TO_CACHE_KEY, key=key, value=value)
        return cached

    @staticmethod
    def get_etag(cached_data: Union[str, bytes, Dict]) -> str:
        if isinstance(cached_data, bytes):
            cached_data = cached_data.decode()
        if not isinstance(cached_data, str):
            cached_data = BetterJsonEncoder().encode(cached_data)
        return f"W/{hash(cached_data)}"


class BetterJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return {"val": obj.isoformat(), "_spec_type": str(type(obj))}
        elif isinstance(obj, Decimal):
            return {"val": str(obj), "_spec_type": str(Decimal)}
        elif isinstance(obj, Page):
            return jsonable_encoder(obj)
        else:
            return super().default(obj)


def calculate_ttl(expire: Union[int, timedelta]) -> int:
    """Converts expire time to total seconds and ensures that ttl is capped at one year."""
    if isinstance(expire, timedelta):
        expire = int(expire.total_seconds())
    return min(expire, ONE_YEAR_IN_SECONDS)


async def get_api_response_async(func, *args, **kwargs):
    """Helper function that allows decorator to work with both async and non-async functions."""
    return (
        await func(*args, **kwargs)
        if asyncio.iscoroutinefunction(func)
        else func(*args, **kwargs)
    )


def cache_with_key_builder(
    *, expire: Union[int, timedelta] = ONE_YEAR_IN_SECONDS, key_builder=None
):
    def outer_wrapper(func):
        @wraps(func)
        async def inner_wrapper(*args, **kwargs):
            func_kwargs = kwargs.copy()
            request = func_kwargs.pop("request", None)
            response = func_kwargs.pop("response", None)
            create_response_directly = not response
            if create_response_directly:
                response = Response()
            redis_cache = CustomFastApiRedisCache()
            if redis_cache.not_connected or redis_cache.request_is_not_cacheable(
                request
            ):
                return await get_api_response_async(func, *args, **kwargs)

            # Use the custom key builder if it's provided
            key = (
                key_builder(func, *args, **kwargs)
                if key_builder
                else redis_cache.get_cache_key(func, *args, **kwargs)
            )

            ttl, in_cache = redis_cache.check_cache(key)
            if in_cache:
                redis_cache.set_response_headers(
                    response, True, deserialize_json(in_cache), ttl
                )
                if redis_cache.requested_resource_not_modified(request, in_cache):
                    response.status_code = int(HTTPStatus.NOT_MODIFIED)
                    return (
                        Response(
                            content=None,
                            status_code=response.status_code,
                            media_type="application/json",
                            headers=response.headers,
                        )
                        if create_response_directly
                        else response
                    )
                return (
                    Response(
                        content=in_cache,
                        media_type="application/json",
                        headers=response.headers,
                    )
                    if create_response_directly
                    else deserialize_json(in_cache)
                )
            response_data = await get_api_response_async(func, *args, **kwargs)
            ttl = calculate_ttl(expire)
            cached = redis_cache.add_to_cache(key, response_data, ttl)
            if cached:
                redis_cache.set_response_headers(
                    response, cache_hit=False, response_data=response_data, ttl=ttl
                )
                return (
                    Response(
                        content=serialize_json(response_data),
                        media_type="application/json",
                        headers=response.headers,
                    )
                    if create_response_directly
                    else response_data
                )
            return response_data

        return inner_wrapper

    return outer_wrapper


def serialize_json(json_dict):
    return json.dumps(json_dict, cls=BetterJsonEncoder)


def custom_cache(expire: int, ignore_args: list = None):
    if ignore_args is None:
        ignore_args = []

    def custom_key_builder(f, *f_args, **f_kwargs):
        new_kwargs = {k: v for k, v in f_kwargs.items() if k not in ignore_args}
        key = CustomFastApiRedisCache().get_cache_key(f, *f_args, **new_kwargs)
        return key

    def outer_wrapper(func):
        @wraps(func)
        async def inner_wrapper(*args, **kwargs):
            func_kwargs = kwargs.copy()
            request = func_kwargs.pop("request", None)
            response = func_kwargs.pop("response", None)
            create_response_directly = not response
            if create_response_directly:
                response = Response()
            redis_cache = CustomFastApiRedisCache()
            if redis_cache.not_connected or redis_cache.request_is_not_cacheable(
                request
            ):
                return await get_api_response_async(func, *args, **kwargs)

            key = custom_key_builder(func, *args, **kwargs)

            ttl, in_cache = redis_cache.check_cache(key)
            if in_cache:
                redis_cache.set_response_headers(
                    response, True, deserialize_json(in_cache), ttl
                )
                if redis_cache.requested_resource_not_modified(request, in_cache):
                    response.status_code = int(HTTPStatus.NOT_MODIFIED)
                    return (
                        Response(
                            content=None,
                            status_code=response.status_code,
                            media_type="application/json",
                            headers=response.headers,
                        )
                        if create_response_directly
                        else response
                    )
                return (
                    Response(
                        content=in_cache,
                        media_type="application/json",
                        headers=response.headers,
                    )
                    if create_response_directly
                    else deserialize_json(in_cache)
                )
            response_data = await get_api_response_async(func, *args, **kwargs)
            ttl = calculate_ttl(expire)
            cached = redis_cache.add_to_cache(key, response_data, ttl)
            if cached:
                redis_cache.set_response_headers(
                    response, cache_hit=False, response_data=response_data, ttl=ttl
                )
                return (
                    Response(
                        content=serialize_json(response_data),
                        media_type="application/json",
                        headers=response.headers,
                    )
                    if create_response_directly
                    else response_data
                )
            return response_data

        return inner_wrapper

    return outer_wrapper
