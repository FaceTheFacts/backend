import pytest

from src.db.models.party import Party


class TestParty:
    def test_insert_party_valid(self, session):
        # Act
        party = Party(
            id=1,
            entity_type="party",
            label="CDU",
            api_url="https://www.abgeordnetenwatch.de/api/parties/1",
            full_name="Christlich Demokratische Union Deutschlands",
            short_name="CDU",
        )
        session.add(party)
        session.commit()
        result = session.query(Party).filter(Party.id == 1).first()
        # Assert
        assert result.entity_type == "party"
        assert result.label == "CDU"
        assert result.api_url == "https://www.abgeordnetenwatch.de/api/parties/1"
        assert result.full_name == "Christlich Demokratische Union Deutschlands"
        assert result.short_name == "CDU"

    @pytest.mark.xfail(raises=Exception)
    def test_insert_party_only_id_and_entity_invalid(self, session):
        # Act
        party = Party(
            id=1,
            entity_type="party",
        )
        session.add(party)
        try:
            session.commit()
        except Exception:
            session.rollback()
