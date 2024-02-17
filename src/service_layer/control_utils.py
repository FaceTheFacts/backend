# std
import logging
import requests
import math
from typing import List

# local
from src.logging_config import configure_logging
from src.api.repository import SqlAlchemyBaseRepository
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


def prepare_vote_data(missing_votes):
    return [
        {
            "id": ap.get("id"),
            "entity_type": ap.get("entity_type"),
            "label": ap.get("label"),
            "api_url": ap.get("api_url"),
            "mandate_id": ap["mandate"]["id"] if ap.get("mandate") else None,
            "fraction_id": ap["fraction"]["id"] if ap.get("fraction") else None,
            "poll_id": ap["poll"]["id"] if ap.get("poll") else None,
            "vote": ap.get("vote"),
            "reason_no_show": ap.get("reason_no_show"),
            "reason_no_show_other": ap.get("reason_no_show_other"),
        }
        for ap in missing_votes
    ]


def prepare_party_data(api_parties):
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
    return party_styles, parties


def prepare_politician_data(api_politicians):
    return [
        {
            "id": ap["id"],
            "entity_type": ap.get("entity_type"),
            "label": ap.get("label"),
            "api_url": ap.get("api_url"),
            "first_name": ap.get("first_name"),
            "last_name": ap.get("last_name"),
            "sex": ap.get("sex"),
            "year_of_birth": ap.get("year_of_birth"),
            "party_id": ap["party"]["id"] if ap.get("party") else None,
            "party_past": ap.get("party_past"),
            "deceased": None,
            "deceased_date": None,
            "education": ap.get("education"),
            "residence": ap.get("residence"),
            "occupation": ap.get("occupation"),
            "statistic_questions": ap.get("statistic_questions"),
            "statistic_questions_answered": ap.get("statistic_questions_answered"),
            "qid_wikidata": ap.get("qid_wikidata"),
            "field_title": ap.get("field_title"),
        }
        for ap in api_politicians
    ]
