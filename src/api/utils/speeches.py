import math
import re
from typing import Optional

from src.api.utils.read_url import load_json_from_url
from src.cron_jobs.utils.file import write_json
from src.db import models
from src.db.connection import Session


def clean_text(text: str) -> str:
    # Remove non-printable characters except common whitespace characters
    text = re.sub(r"[^\x20-\x7E\t\n\r\f\väöüÄÖÜß]", " ", text)
    return text


def is_politician_comment(text: str) -> bool:
    pattern = r"\((Dr\.\s*)?[\w\s]+(\s\[[\w/]+\])?:"
    return bool(re.search(pattern, text))


def extract_comment(text: str) -> str:
    pattern = r"\((?:Dr\.\s*)?[\w\s]+(?:\s\[[\w/]+\])?:\s*"
    cleaned_text = re.sub(pattern, "", text)
    cleaned_text = cleaned_text.strip()
    if cleaned_text.endswith(")"):
        cleaned_text = cleaned_text[:-1]
    return cleaned_text


def extract_politician_name(text: str) -> str:
    # A regex pattern that matches a politician's name, an optional title, and a party name abbreviation
    pattern = r"\((Dr\.\s*)?([\w\s]+)(\s\[[\w/]+\])?:"
    match = re.match(pattern, text)
    if match:
        return match.group(2)
    return ""


PARLIAMENT_PERIOD_TO_ELECTORIAL_PERIOD_DICT = {
    20: 128,
    19: 111,
}
