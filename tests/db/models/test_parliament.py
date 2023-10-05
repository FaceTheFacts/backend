from src.db.models.parliament import Parliament


def test_insert_parliament(session):
    parliament = Parliament(
        id=1,
        entity_type="parliament",
        label="1. Wahlperiode",
        api_url="https://www.abgeordnetenwatch.de/api/parliaments/1",
        abgeordnetenwatch_url="https://www.abgeordnetenwatch.de/api/parliaments/1",
        label_external_long="1. Wahlperiode (1949-1953)",
    )
    session.add(parliament)
    session.commit()
    result = session.query(Parliament).filter(Parliament.id == 1).first()
    assert result.entity_type == "parliament"
    assert result.label == "1. Wahlperiode"
    assert result.api_url == "https://www.abgeordnetenwatch.de/api/parliaments/1"
    assert (
        result.abgeordnetenwatch_url
        == "https://www.abgeordnetenwatch.de/api/parliaments/1"
    )
