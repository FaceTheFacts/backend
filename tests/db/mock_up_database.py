# local
import src.db.models as models

# default
from unittest import mock

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
    ]
)
