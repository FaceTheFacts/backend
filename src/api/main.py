# std
from typing import Optional
import time
import threading
import os

# third-party
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import schedule
from fastapi_redis_cache import cache
from redis import asyncio as aioredis
from sqlalchemy.orm.session import Session


# local
from src.api.versions import v1, plugin
from src.api.utils.openapi import api_description, tags_metadata
import src.cron_jobs.append_db as cron_jobs
from src.redis_cache.cache import LOCAL_REDIS_URL, CustomFastApiRedisCache, get_redis


app = FastAPI(
    title="FaceTheFacts API",
    description=api_description,
    version="1.0",
    terms_of_service="https://facethefacts.app/legal-notice",
    contact={
        "name": "FaceTheFacts",
        "url": "https://facethefacts.app/contact",
        "email": "info@facethefacts.app",
    },
    license_info={
        "name": "GNU GENERAL PUBLIC LICENSE Version 3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
    openapi_tags=tags_metadata,
)


# Initialize FastAPI Redis Cache on startup
@app.on_event("startup")
def startup():
    redis_cache = CustomFastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="FaceTheFacts-cache",
        ignore_arg_types=[Request, Response, Session],
        response_header="X-FaceTheFacts-API-Cache",
    )


# List all versions here
app.include_router(plugin.router)
app.include_router(v1.router)

# CORS-policy
# * docs: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Cache-Control"] = "no-store"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js 'sha256-R2r7jpC1j6BEeer9P/YDRn6ufsaSnnARhKTdfrSKStk='; style-src 'self' https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css; frame-ancestors 'none'"

    # HTML-related (future-proof)
    response.headers["Feature-Policy"] = "'none'"
    response.headers["Referrer-Policy"] = "no-referrer"

    return response


@app.get("/health_check")
async def health_check(redis_pool: aioredis.Redis = Depends(get_redis)):
    pong = await redis_pool.ping()
    print(f"Ping result: {pong}")
    if pong != True:
        raise HTTPException(status_code=500, detail="Redis server is not responding")
    return {"status": "OK", "detail": "Redis server is responding"}


@app.get("/")
@cache(expire=60)
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return FileResponse(filename, media_type="image/png")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return Response(text, media_type="application/json")


def scheduled_task():
    schedule.every().monday.at("02:50").do(cron_jobs.append_committees)
    schedule.every().monday.at("03:00").do(cron_jobs.append_committee_memberships)
    schedule.every().monday.at("03:10").do(cron_jobs.append_candidacies)
    schedule.every().monday.at("03:20").do(cron_jobs.append_sidejobs)
    schedule.every().monday.at("03:30").do(cron_jobs.append_polls)
    schedule.every().monday.at("03:40").do(cron_jobs.append_votes)
    schedule.every().monday.at("03:50").do(cron_jobs.append_vote_results)
    schedule.every().monday.at("04:00").do(cron_jobs.append_parties)
    schedule.every().monday.at("04:10").do(cron_jobs.append_politicians)

    print("Cronjob executed!")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    t1 = threading.Thread(target=scheduled_task, daemon=True)
    t1.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
