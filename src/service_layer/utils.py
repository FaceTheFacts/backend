# std
import logging
import requests
import math
from typing import List

# local
from src.domain.entities import Entity
from src.logging_config import configure_logging
from src.api.repository import SqlAlchemyBaseRepository, SqlAlchemyFactory
import src.db.models as models


configure_logging()
logger = logging.getLogger(__name__)


class FetchMissingEntity:
    def __init__(
        self,
        entity: str,
        repo: SqlAlchemyBaseRepository,
        base_url: str = "https://www.abgeordnetenwatch.de/api/v2",
        page_size=1000,
    ):
        self.entity = entity
        self.base_url = base_url
        self.repo = repo
        self.page_size = page_size
        self.total_abgeordnetenwatch_entity = self.count_abgeordnetenwatch_entity()
        self.total_database_entity = self.count_database_entity()
        self.is_missing_entity = self.check_is_missing_entity()
        self.last_id = self.get_last_id() if self.total_database_entity > 0 else 0
        self.page_count = self.count_pages()

    def count_abgeordnetenwatch_entity(self) -> int:
        url = f"{self.base_url}/{self.entity}?range_end=0"
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = response.json()
            total = results["meta"]["result"]["total"]
            return total
        except requests.exceptions.ConnectionError as e:
            logger.error("Internet connection error: %s", e)
            return 0

    def count_database_entity(self) -> int:
        return self.repo.count()

    def check_is_missing_entity(self):
        if self.total_abgeordnetenwatch_entity > self.total_database_entity:
            logger.info(
                f"Missing {self.total_abgeordnetenwatch_entity - self.total_database_entity} {self.entity} entity"
            )
            return True
        else:
            logger.info(f"No missing {self.entity} entity")
            return False

    def get_last_id(self):
        return self.repo.get_last_id()

    def count_pages(self) -> int:
        if self.is_missing_entity:
            url = f"https://www.abgeordnetenwatch.de/api/v2/{self.entity}?id[gt]={self.last_id}&range_end=0"
            try:
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()
                total = result["meta"]["result"]["total"]
                if total == 0:
                    return 0
                page_count = math.ceil(total / self.page_size)
                return page_count
            except requests.exceptions.ConnectionError as e:
                logger.error("Internet connection error: %s", e)
                return 0
        else:
            return 0

    def fetch_missing_entities(self) -> List[models.Party]:
        if not self.is_missing_entity:
            return []
        data_list = []
        for page_num in range(self.page_count):
            url = f"https://www.abgeordnetenwatch.de/api/v2/{self.entity}?id[gt]={self.last_id}&page={page_num}&pager_limit={self.page_size}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()
                data = result["data"]
                for item in data:
                    data_list.append(item)
            except requests.exceptions.ConnectionError as e:
                logger.error("Internet connection error: %s", e)
                return []
        return data_list


def prepare_party_style_data(api_parties):
    party_styles = [
        {
            "id": ap.get("id"),
            "display_name": ap.get("label"),
            "foreground_color": "#FFFFFF",
            "background_color": "#333333",
            "border_color": None,
        }
        for ap in api_parties
    ]

    return party_styles


def prepare_party_data(api_parties):
    parties = [
        {
            "id": ap["id"],
            "entity_type": ap.get("entity_type"),
            "label": ap.get("label"),
            "api_url": ap.get("api_url"),
            "full_name": ap.get("full_name"),
            "short_name": ap.get("short_name"),
            "party_style_id": ap["id"],
        }
        for ap in api_parties
    ]
    return parties


def prepare_parliament_data(api_parliaments):
    parliaments = [
        {
            "id": api_parliament["id"],
            "entity_type": api_parliament["entity_type"],
            "label": api_parliament["label"],
            "api_url": api_parliament["api_url"],
            "abgeordnetenwatch_url": api_parliament["abgeordnetenwatch_url"],
            "label_external_long": api_parliament["label_external_long"],
        }
        for api_parliament in api_parliaments
    ]
    return parliaments


def prepare_parliament_period_data(api_parliament_periods):
    parliament_periods = [
        {
            "id": api_parliament_period["id"],
            "entity_type": api_parliament_period["entity_type"],
            "label": api_parliament_period["label"],
            "api_url": api_parliament_period["api_url"],
            "abgeordnetenwatch_url": api_parliament_period["abgeordnetenwatch_url"],
            "type": api_parliament_period["type"],
            "election_date": api_parliament_period["election_date"],
            "start_date_period": api_parliament_period["start_date_period"],
            "end_date_period": api_parliament_period["end_date_period"],
            "parliament_id": api_parliament_period["parliament"]["id"],
            "previous_period_id": (
                api_parliament_period["previous_period"]["id"]
                if api_parliament_period["previous_period"]
                else None
            ),
        }
        for api_parliament_period in api_parliament_periods
    ]
    return parliament_periods


def prepare_topic_data(api_topics):
    topics = [
        {
            "id": api_topic["id"],
            "entity_type": api_topic["entity_type"],
            "label": api_topic["label"],
            "api_url": api_topic["api_url"],
            "abgeordnetenwatch_url": api_topic["abgeordnetenwatch_url"],
            "description": api_topic["description"],
            "parent_id": api_topic["parent"][0]["id"] if api_topic["parent"] else None,
        }
        for api_topic in api_topics
    ]
    return topics


def prepare_committee_data(api_committees):
    committees = [
        {
            "id": api_committee["id"],
            "entity_type": api_committee["entity_type"],
            "label": api_committee["label"],
            "api_url": api_committee["api_url"],
            "field_legislature_id": api_committee["field_legislature"]["id"],
        }
        for api_committee in api_committees
    ]

    return committees


def prepare_committee_has_topic_data(api_committees):
    committee_topics = []
    for api_committee in api_committees:
        if api_committee["field_topics"] is not None:
            for topic in api_committee["field_topics"]:
                committee_topics.append(
                    {
                        "committee_id": api_committee["id"],
                        "topic_id": topic["id"],
                    }
                )
    return committee_topics


def prepare_poll_data(api_polls):
    polls = [
        {
            "id": api_poll["id"],
            "entity_type": api_poll["entity_type"],
            "label": api_poll["label"],
            "api_url": api_poll["api_url"],
            "field_committees_id": (
                api_poll["field_committees"][0]["id"]
                if api_poll["field_committees"]
                else None
            ),
            "field_intro": api_poll["field_intro"],
            "field_legislature_id": (
                api_poll["field_legislature"]["id"]
                if api_poll["field_legislature"]
                else None
            ),
            "field_poll_date": api_poll["field_poll_date"],
        }
        for api_poll in api_polls
    ]
    return polls


def prepare_politician_data(api_politicians):
    politicians = [
        {
            {
                "id": api_politician["id"],
                "entity_type": api_politician["entity_type"],
                "label": api_politician["label"],
                "api_url": api_politician["api_url"],
                "abgeordnetenwatch_url": api_politician["abgeordnetenwatch_url"],
                "first_name": api_politician["first_name"],
                "last_name": api_politician["last_name"],
                "birth_name": api_politician["birth_name"],
                "sex": api_politician["sex"],
                "year_of_birth": api_politician["year_of_birth"],
                "party_id": (
                    api_politician["party"]["id"] if api_politician["party"] else None
                ),
                "party_past": api_politician["party_past"],
                "deceased": None,
                "deceased_date": None,
                "education": api_politician["education"],
                "residence": api_politician["residence"],
                "occupation": api_politician["occupation"],
                "statistic_questions": api_politician["statistic_questions"],
                "statistic_questions_answered": api_politician[
                    "statistic_questions_answered"
                ],
                "qid_wikidata": api_politician["qid_wikidata"],
                "field_title": api_politician["field_title"],
            }
        }
        for api_politician in api_politicians
    ]
    return politicians
