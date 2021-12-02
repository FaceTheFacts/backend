# local
import src.db.models as models

# default
from unittest import mock
import datetime

# third-party
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import or_

mockup_session = UnifiedAlchemyMagicMock(
    data=[
        # Politician
        (
            [
                mock.call.query(models.Politician),
                mock.call.filter(models.Politician.id == 1),
            ],
            [models.Politician(id=1, label="Christian Lindner")],
        ),
        (
            [
                mock.call.query(models.Politician),
                mock.call.filter(models.Politician.id == 2),
            ],
            [models.Politician(id=2, label="Philipp Amthor")],
        ),
        # CandidacyMandate
        (
            [
                mock.call.query(models.CandidacyMandate),
                mock.call.filter(
                    models.Politician.id == 1,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                ),
            ],
            [models.CandidacyMandate(id=1, label="Christian Lindner(2020)")],
        ),
        (
            [
                mock.call.query(models.CandidacyMandate),
                mock.call.filter(
                    models.Politician.id == 2,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                ),
            ],
            [models.CandidacyMandate(id=2, label="Philipp Amthor(2020)")],
        ),
        # SidejobHasMandate
        (
            [
                mock.call.query(models.SidejobHasMandate),
                mock.call.filter(
                    models.Politician.id == 1,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                    models.CandidacyMandate.id
                    == models.SidejobHasMandate.candidacy_mandate_id,
                ),
            ],
            [
                models.SidejobHasMandate(sidejob_id=1, candidacy_mandate_id=1),
                models.SidejobHasMandate(sidejob_id=2, candidacy_mandate_id=1),
            ],
        ),
        (
            [
                mock.call.query(models.SidejobHasMandate),
                mock.call.filter(
                    models.Politician.id == 2,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                    models.CandidacyMandate.id
                    == models.SidejobHasMandate.candidacy_mandate_id,
                ),
            ],
            [models.SidejobHasMandate(sidejob_id=1, candidacy_mandate_id=2)],
        ),
        # Sidejob
        (
            [
                mock.call.query(models.Sidejob),
                mock.call.filter(
                    models.Politician.id == 1,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                    models.CandidacyMandate.id
                    == models.SidejobHasMandate.candidacy_mandate_id,
                    models.SidejobHasMandate.sidejob_id == models.Sidejob.id,
                ),
            ],
            [
                models.Sidejob(
                    id=1, label="Member of the County Council", income_level="1"
                ),
                models.Sidejob(id=2, label="Chairman", income_level="2"),
            ],
        ),
        (
            [
                mock.call.query(models.Sidejob),
                mock.call.filter(
                    models.Politician.id == 2,
                    models.Politician.id == models.CandidacyMandate.politician_id,
                    models.CandidacyMandate.id
                    == models.SidejobHasMandate.candidacy_mandate_id,
                    models.SidejobHasMandate.sidejob_id == models.Sidejob.id,
                ),
            ],
            [models.Sidejob(id=2, label="Chairman", income_level="2")],
        ),
        # Poll
        (
            [
                mock.call.query(models.Poll),
                mock.call.filter(models.Poll.field_legislature_id == 1),
            ],
            [
                models.Poll(
                    id=1,
                    field_legislature_id=1,
                    label="CDU voting right",
                    field_poll_date=datetime.datetime(2021, 10, 1),
                ),
                models.Poll(
                    id=2,
                    field_legislature_id=1,
                    label="CDU voting right",
                    field_poll_date=datetime.datetime(2021, 9, 1),
                ),
            ],
        ),
        (
            [
                mock.call.query(models.Poll),
                mock.call.filter(
                    or_(
                        models.Poll.field_legislature_id == 111,
                        models.Poll.field_legislature_id == 132,
                    )
                ),
                mock.call.order_by(models.Poll.field_poll_date.desc()),
            ],
            [
                models.Poll(
                    id=3,
                    field_legislature_id=111,
                    label="CDU voting right",
                    field_poll_date=datetime.datetime(2021, 10, 1),
                ),
                models.Poll(
                    id=4,
                    field_legislature_id=111,
                    label="CDU voting right",
                    field_poll_date=datetime.datetime(2021, 9, 27),
                ),
                models.Poll(
                    id=5,
                    field_legislature_id=132,
                    label="Amendment to the Infection Protection Act",
                    field_poll_date=datetime.datetime(2021, 9, 20),
                ),
                models.Poll(
                    id=6,
                    field_legislature_id=132,
                    label="Amendment to the Infection Protection Act",
                    field_poll_date=datetime.datetime(2021, 9, 18),
                ),
            ],
        ),
    ]
)
