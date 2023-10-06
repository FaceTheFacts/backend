from src.db.models.party import Party


# Test populate_parties later
# def test_insert_party(session):
#     party = Party(
#         id=1,
#         entity_type="party",
#         label="CDU",
#         api_url="https://www.abgeordnetenwatch.de/api/parties/1",
#         full_name="Christlich Demokratische Union Deutschlands",
#         short_name="CDU",
#     )
#     session.add(party)
#     session.commit()
#     result = session.query(Party).filter(Party.id == 1).first()
#     session.close()
#     assert result.entity_type == "party"
#     assert result.label == "CDU"
#     assert result.api_url == "https://www.abgeordnetenwatch.de/api/parties/1"
#     assert result.full_name == "Christlich Demokratische Union Deutschlands"
#     assert result.short_name == "CDU"
