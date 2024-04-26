# std
import abc
from typing import Optional, List, Dict, Any

# third-party
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import inspect

# local
import src.db.models as models
from src.domain.entities import Entity


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
        self.primary_keys = [key.name for key in inspect(self.model_class).primary_key]

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

    def add_or_update_list(self, entities: List[Dict[str, Any]]):
        stmt = insert(self.model_class).values(entities)
        update_dict = {col.name: col for col in stmt.excluded if not col.primary_key}

        if update_dict:
            stmt = stmt.on_conflict_do_update(
                index_elements=self.primary_keys,
                set_=update_dict,
            )
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=self.primary_keys)

        self.session.execute(stmt)
        self.session.commit()

    def count(self):
        return self.session.query(self.model_class).count()

    def get_last_id(self):
        return (
            self.session.query(self.model_class.id)
            .order_by(self.model_class.id.desc())
            .first()
            .id
        )


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


class SqlAlchemyPartyStyleRepository(SqlAlchemyBaseRepository):
    """Repository class for PartyStyle"""

    def __init__(self, session):
        super().__init__(session, models.PartyStyle)


class SqlAlchemyParliamentRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Parliament)


class SqlAlchemyParliamentPeriodRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.ParliamentPeriod)


class SqlAlchemyTopicRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Topic)


class SqlAlchemyCommitteeRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Committee)


class SqlAlchemyCommitteeHasTopicRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.CommitteeHasTopic)


class SqlAlchemyPollRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Poll)


class SqlAlchemyVoteRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Vote)


class SqlAlchemyPoliticianRepository(SqlAlchemyBaseRepository):
    def __init__(self, session):
        super().__init__(session, models.Politician)


class SqlAlchemyFactory:
    """Factory class to create repositories"""

    def __init__(self, session):
        self.session = session
        """Must add new repositories to the map to be able to create them"""
        self.entity_factory_map = {
            Entity.PARTY.value: self.create_party_repository,
            Entity.PARTY_STYLE.value: self.create_party_style_repository,
            Entity.POLITICIAN.value: self.create_politician_repository,
            Entity.PARLIAMENT.value: self.create_parliament_repository,
            Entity.PARLIAMENT_PERIOD.value: self.create_parliament_period_repository,
            Entity.TOPIC.value: self.create_topic_repository,
            Entity.COMMITTEE.value: self.create_committee_repository,
            Entity.COMMITTEE_HAS_TOPIC.value: self.create_committee_has_topic_repository,
            Entity.POLL.value: self.create_poll_repository,
        }

    def get_repository(
        self, entity: Entity | str
    ) -> Optional[SqlAlchemyBaseRepository]:
        if entity in self.entity_factory_map:
            return self.entity_factory_map[entity]()
        else:
            return None

    def create_party_donation_repository(self) -> SqlAlchemyPartyDonationRepository:
        return SqlAlchemyPartyDonationRepository(self.session)

    # in the map
    def create_party_repository(self) -> SqlAlchemyPartyRepository:
        return SqlAlchemyPartyRepository(self.session)

    # in the map
    def create_party_style_repository(self) -> SqlAlchemyPartyStyleRepository:
        return SqlAlchemyPartyStyleRepository(self.session)

    # in the map
    def create_parliament_repository(self) -> SqlAlchemyParliamentRepository:
        return SqlAlchemyParliamentRepository(self.session)

    # in the map
    def create_parliament_period_repository(
        self,
    ) -> SqlAlchemyParliamentPeriodRepository:
        return SqlAlchemyParliamentPeriodRepository(self.session)

    # in the map
    def create_topic_repository(
        self,
    ) -> SqlAlchemyTopicRepository:
        return SqlAlchemyTopicRepository(self.session)

    # in the map
    def create_committee_repository(
        self,
    ) -> SqlAlchemyCommitteeRepository:
        return SqlAlchemyCommitteeRepository(self.session)

    # in the map
    def create_committee_has_topic_repository(
        self,
    ) -> SqlAlchemyCommitteeHasTopicRepository:
        return SqlAlchemyCommitteeHasTopicRepository(self.session)

    # in the map
    def create_poll_repository(
        self,
    ) -> SqlAlchemyPollRepository:
        return SqlAlchemyPollRepository(self.session)

    def create_vote_repository(self) -> SqlAlchemyVoteRepository:
        return SqlAlchemyVoteRepository(self.session)

    def create_politician_repository(self) -> SqlAlchemyPoliticianRepository:
        return SqlAlchemyPoliticianRepository(self.session)
