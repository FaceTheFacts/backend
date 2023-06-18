from slowapi import Limiter
from slowapi.util import get_remote_address
from src.redis_cache.cache import redis_url

limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url)