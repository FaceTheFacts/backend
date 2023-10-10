import abc
from typing import Optional
import src.db.models as models


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, party_donation):
        self.session.add(party_donation)

    # 1.x style
    def get(self, key, value) -> Optional[models.PartyDonation]:
        filter_criteria = {key: value}
        return (
            self.session.query(models.PartyDonation)
            .filter_by(**filter_criteria)
            .one_or_none()
        )
