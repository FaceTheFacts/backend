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
            logger.info(f"No missing {self.entity} entity")
            return 0

    def fetch_missing_entities(self) -> List[models.Party]:
        if not self.is_missing_entity:
            logger.info(f"No missing {self.entity} entity")
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
        if not data_list:
            logger.info(f"No missing {self.entity} entity")
            return data_list
        else:
            return data_list
