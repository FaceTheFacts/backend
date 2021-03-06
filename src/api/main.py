# std
from typing import Optional
import time
import threading

# third-party
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import schedule

# local
from src.api.versions import v1
import src.cron_jobs.append_db as cron_jobs
import src.cron_jobs.crud_db as db_cron_jobs

app = FastAPI()

# List all versions here
app.include_router(v1.router)

# CORS-policy
# * docs: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=["*"])


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


@app.get("/")
def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


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
