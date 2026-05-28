import os
from typing import List


def get_cors_allowed_origins() -> List[str]:
    raw_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    return [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]
