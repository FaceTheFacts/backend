import abc
from typing import Optional, List
import src.db.models as models


class AbstractRepository(abc.ABC):
    """Abstract repository class to be inherited by concrete implementations"""

    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError


class SqlAlchemyBaseRepository(AbstractRepository):
    """Base repository class for SQL Alchemy"""

    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def get(self, key, value):
        filter_criteria = {key: value}
        return (
            self.session.query(self.model_class)
            .filter_by(**filter_criteria)
            .one_or_none()
        )

    def add_or_update(self, entity):
        self.session.merge(entity)
        self.session.commit()


class SqlAlchemyPartyDonationRepository(SqlAlchemyBaseRepository):
    """Repository class for PartyDonation"""

    def __init__(self, session):
        super().__init__(session, models.PartyDonation)

    def list(self, party_ids: Optional[List[int]] = None) -> List[models.PartyDonation]:
        if party_ids is None:
            return (
                self.session.query(self.model_class)
                .order_by(self.model_class.date.desc())
                .all()
            )
        else:
            return (
                self.session.query(self.model_class)
                .where(self.model_class.party_id.in_(party_ids))
                .order_by(self.model_class.date.desc())
                .all()
            )


class SqlAlchemyPartyRepository(SqlAlchemyBaseRepository):
    """Repository class for Party"""

    def __init__(self, session):
        super().__init__(session, models.Party)

    def list(self) -> List[models.Party]:
        return (
            self.session.query(self.model_class)
            .order_by(self.model_class.id.asc())
            .all()
        )


class SqlAlchemyFactory:
    """Factory class to create repositories"""

    def __init__(self, session):
        self.session = session

    def create_party_donation_repository(self) -> SqlAlchemyPartyDonationRepository:
        return SqlAlchemyPartyDonationRepository(self.session)

    def create_party_repository(self) -> SqlAlchemyPartyRepository:
        return SqlAlchemyPartyRepository(self.session)
