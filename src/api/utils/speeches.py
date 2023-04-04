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


def fetch_speech_data(page: int, abgeordnetenwatch_id: Optional[int] = None):
    url = f"https://de.openparliament.tv/api/v1/search/media?parliament=DE&page={page}&sort=date-desc"
    if abgeordnetenwatch_id:
        url = f"https://de.openparliament.tv/api/v1/search/media?abgeordnetenwatchID={abgeordnetenwatch_id}&page={page}&sort=date-desc"

    raw_data = load_json_from_url(url)

    total = raw_data["meta"]["results"]["total"]
    if total == 0:
        return None

    last_page = math.ceil(total / 40)
    if last_page < page:
        return None

    return raw_data


def process_speech_data(
    db: Optional[Session],
    get_entity_by_id_func,
    get_politician_with_mandate_by_name_func,
    page: int,
    raw_data,
    abgeordnetenwatch_id: Optional[int] = None,
):
    speech_list = []
    for item in raw_data["data"]:
        if item["annotations"]["data"][0]["attributes"]["additionalInformation"][
            "role"
        ] in [
            "Bundestagspräsidentin",
            "Bundestagspräsident",
            "Bundestagsvizepräsidentin",
            "Bundestagsvizepräsident",
        ]:
            continue
        attributes = item["attributes"]
        if len(item["relationships"]["people"]["data"]) == 0:
            continue
        if abgeordnetenwatch_id:
            attributes = item["attributes"]
            speech_item = {
                "videoFileURI": attributes["videoFileURI"],
                "title": item["relationships"]["agendaItem"]["data"]["attributes"][
                    "title"
                ],
                "date": attributes["dateStart"],
            }
            speech_list.append(speech_item)
        else:
            politician_id = item["relationships"]["people"]["data"][0]["attributes"][
                "additionalInformation"
            ]["abgeordnetenwatchID"]
            speaker = get_entity_by_id_func(db, models.Politician, int(politician_id))
            speech_item = {
                "id": item["id"][3:],
                "videoFileURI": attributes["videoFileURI"],
                "title": item["relationships"]["agendaItem"]["data"]["attributes"][
                    "title"
                ],
                "date": attributes["dateStart"],
                "politician_id": speaker.id,
                "session": item["relationships"]["session"]["data"]["id"],
                "parliament_period_id": PARLIAMENT_PERIOD_TO_ELECTORIAL_PERIOD_DICT[
                    item["relationships"]["electoralPeriod"]["data"]["attributes"][
                        "number"
                    ]
                ],
            }
            speech_item["text"] = []
            for text in attributes["textContents"][0]["textBody"]:
                sentence_obj = {}
                cleaned_text = []
                if text["type"] == "speech":
                    last_sentence_index = len(text["sentences"]) - 1
                    for i, sentence in enumerate(text["sentences"]):
                        if not sentence_obj:
                            sentence_obj["start"] = sentence["timeStart"]
                        # When the current index is the last index, we add the end time
                        if i == last_sentence_index:
                            sentence_obj["end"] = sentence["timeEnd"]
                        cleaned_text.append(clean_text(sentence["text"]))
                    sentence_obj["text"] = cleaned_text
                    speech_item["text"].append(sentence_obj)
                elif text["type"] == "comment":
                    if is_politician_comment(text["sentences"][0]["text"]):
                        extracted_comment = extract_comment(
                            text["sentences"][0]["text"]
                        )
                        cleaned_text.append(clean_text(extracted_comment))
                        sentence_obj["start"] = text["sentences"][0]["timeStart"]
                        sentence_obj["end"] = text["sentences"][0]["timeEnd"]
                        sentence_obj["politician_name"] = extract_politician_name(
                            text["sentences"][0]["text"]
                        )
                        politician = get_politician_with_mandate_by_name_func(
                            db,
                            sentence_obj["politician_name"],
                            speech_item["parliament_period_id"],
                        )
                        if politician:
                            sentence_obj["politician_id"] = politician.id
                        else:
                            print(sentence_obj["politician_name"])
                        sentence_obj["text"] = cleaned_text
                        speech_item["text"].append(sentence_obj)
                continue
            file_path = f"{speech_item['politician_id']}_{speech_item['date']}.json"
            write_json(file_path, speech_item)
            speech_list.append(speech_item)

    size = raw_data["meta"]["results"]["count"]
    last_page = math.ceil(raw_data["meta"]["results"]["total"] / 40)
    is_last_page = last_page == page

    fetched_speeches = {
        "items": speech_list,
        "total": raw_data["meta"]["results"]["total"],
        "page": page,
        "size": len(speech_list),
        "is_last_page": is_last_page,
    }
    if abgeordnetenwatch_id:
        fetched_speeches["politician_id"] = abgeordnetenwatch_id

    return fetched_speeches
