from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class SidejobOrganizationHasTopic(Base):
    __tablename__ = "sidejob_organization_has_topic"

    sidejob_organization_id = Column(
        Integer, ForeignKey("sidejob_organization.id"), primary_key=True
    )
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
