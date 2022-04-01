# local
import src.db.models as models

# default
from unittest import mock
import datetime
from sqlalchemy import and_

# third-party
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

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
                    id=1,
                    label="Member of the County Council",
                    income_level="1",
                    entity_type="sidejob",
                    created=1611842082,
                ),
                models.Sidejob(
                    id=2,
                    label="Chairman",
                    income_level="2",
                    entity_type="sidejob",
                    created=1611842082,
                ),
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
                mock.call.filter(models.Poll.field_legislature_id == 132),
                mock.call.order_by(models.Poll.field_poll_date.desc()),
            ],
            [
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
        # VoteResult
        (
            [
                mock.call.query(models.VoteResult),
                mock.call.filter(models.VoteResult.poll_id == 5),
            ],
            [
                models.VoteResult(id=1, yes=10, no=10, abstain=0, no_show=2, poll_id=5),
            ],
        ),
        (
            [
                mock.call.query(models.VoteResult),
                mock.call.filter(models.VoteResult.poll_id == 6),
            ],
            [
                models.VoteResult(id=2, yes=10, no=10, abstain=0, no_show=2, poll_id=6),
            ],
        ),
        # latest-polls
        (
            [
                mock.call.query(models.CandidacyMandate),
                mock.call.join(models.Vote),
                mock.call.filter(
                    and_(
                        models.CandidacyMandate.parliament_period_id == 132,
                        models.Vote.poll_id == 5,
                        models.Vote.vote != "no_show",
                    )
                ),
            ],
            [models.CandidacyMandate()],
        ),
    ]
)
