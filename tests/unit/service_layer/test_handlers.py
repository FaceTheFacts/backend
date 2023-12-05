# third-party
from sqlalchemy import text

# local
from src.service_layer import handlers, messagebus, utils
from src.domain import events, commands
from src.api import repository


class TestHandlers:
    """Step1: Fetch missing party data from abgeordnetenwatch.de"""

    def test_fetch_missing_party_with_no_party_exist(self, session):
        # Act
        missing_party_data = messagebus.handle(
            commands.FetchMissingEntity(entity="party", session=session)
        )
        # Assert
        assert missing_party_data != []

    """ Step1: Fetch missing party data from abgeordnetenwatch.de"""

    def test_fetch_missing_party_with_party_exist(
        self, session, setup_sqlite_party_related_tables
    ):
        # Act
        missing_party_data = messagebus.handle(
            commands.FetchMissingEntity(entity="party", session=session)
        )
        # Assert
        assert missing_party_data != []

    """Step2: Prepare data for updating party_style and party tables"""

    def test_prepare_update_data(self):
        # Arrange
        data = [
            {
                "id": 1,
                "entity_type": "party",
                "label": "SPD",
                "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
                "full_name": "Sozialdemokratische Partei Deutschlands",
                "short_name": "SPD",
            },
            {
                "id": 2,
                "entity_type": "party",
                "label": "CDU",
                "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
                "full_name": "Christlich Demokratische Union Deutschlands",
                "short_name": "CDU",
            },
        ]
        # Act
        results = messagebus.handle(
            commands.PrepareUpdateData(entity="party", data=data)
        )
        # Assert
        assert results[0] == {
            "entities": ["party_style", "party"],
            "data": [
                [
                    {
                        "id": 1,
                        "display_name": "SPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                    {
                        "id": 2,
                        "display_name": "CDU",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                ],
                [
                    {
                        "id": 1,
                        "entity_type": "party",
                        "label": "SPD",
                        "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
                        "full_name": "Sozialdemokratische Partei Deutschlands",
                        "short_name": "SPD",
                        "party_style_id": 1,
                    },
                    {
                        "id": 2,
                        "entity_type": "party",
                        "label": "CDU",
                        "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
                        "full_name": "Christlich Demokratische Union Deutschlands",
                        "short_name": "CDU",
                        "party_style_id": 2,
                    },
                ],
            ],
        }

    """Step3: Update party_style and party tables"""

    def test_update_table(self, session):
        # Arrange
        entities = ["party_style", "party"]
        data = [
            [
                {
                    "id": 1,
                    "display_name": "SPD",
                    "foreground_color": "#000000",
                    "background_color": "#FFFFFF",
                    "border_color": "#000000",
                },
                {
                    "id": 2,
                    "display_name": "SPD",
                    "foreground_color": "#000000",
                    "background_color": "#FFFFFF",
                    "border_color": "#000000",
                },
            ],
            [
                {
                    "id": 1,
                    "entity_type": "party",
                    "label": "SPD",
                    "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
                    "full_name": "Sozialdemokratische Partei Deutschlands",
                    "short_name": "SPD",
                    "party_style_id": 1,
                },
                {
                    "id": 2,
                    "entity_type": "party",
                    "label": "CDU",
                    "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
                    "full_name": "Christlich Demokratische Union Deutschlands",
                    "short_name": "CDU",
                    "party_style_id": 2,
                },
            ],
        ]
        # Act
        messagebus.handle(
            commands.UpdateTable(entities=entities, data=data, session=session)
        )
        rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 1})
        # Assert
        assert list(rows) == [
            (
                1,
                "party",
                "SPD",
                "https://www.abgeordnetenwatch.de/api/parties/1",
                "Sozialdemokratische Partei Deutschlands",
                "SPD",
                1,
            )
        ]
        # Cleanup
        session.execute(text("DELETE FROM party_style"))
        session.execute(text("DELETE FROM party"))

    """ Step1 to Step3: Fetch missing party data from abgeordnetenwatch.de, prepare data for updating party_style and party tables, update party_style and party tables"""

    def test_fetch_missing_party_update_table(self, session):
        # Act
        missing_party_data = messagebus.handle(
            commands.FetchMissingEntity(entity="party", session=session)
        )

        prepared_update_data = messagebus.handle(
            commands.PrepareUpdateData(entity="party", data=missing_party_data[0])
        )
        messagebus.handle(
            commands.UpdateTable(
                entities=prepared_update_data[0]["entities"],
                data=prepared_update_data[0]["data"],
                session=session,
            )
        )
        rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 1})
        # Assert
        assert list(rows) == [
            (
                1,
                "party",
                "SPD",
                "https://www.abgeordnetenwatch.de/api/parties/1",
                "Sozialdemokratische Partei Deutschlands",
                "SPD",
                1,
            )
        ]
        # Cleanup
        session.execute(text("DELETE FROM party_style"))
        session.execute(text("DELETE FROM party"))
