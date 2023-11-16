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
        messagebus.handle(events.MissingEntityFetched(entity="party"))
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
        messagebus.handle(events.MissingEntityFetched(entity="party"))
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
        messagebus.handle(events.UpdatedEntityPrepared(entities=results[0]["entities"]))  # type: ignore
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
        messagebus.handle(events.TableUpdated(entities=entities))
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

    # def test_fetch_missing_party_update_table(self, session):
    #     factory = repository.SqlAlchemyFactory(session)
    #     repo = factory.create_party_repository()
    #     missing_party_data = utils.FetchMissingEntity(
    #         "parties", repo
    #     ).fetch_missing_entities()
    #     update_data = messagebus.handle(
    #         events.MissingEntityFetched(entity="party", data=missing_party_data)  # type: ignore
    #     )
    #     messagebus.handle(
    #         events.UpdatedEntityPrepared(
    #             **update_data[0], session=session  # type: ignore
    #         )
    #     )  # type: ignore
    #     rows = session.execute(
    #         text("SELECT * FROM party_style WHERE id = :id"), {"id": 1}
    #     )
    #     # Assert
    #     assert list(rows) == [(1, "SPD", "#000000", "#FFFFFF", "#000000")]
    #     # Act
    #     rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 1})
    #     # # Assert
    #     assert list(rows) == [
    #         (
    #             1,
    #             "party",
    #             "SPD",
    #             "https://www.abgeordnetenwatch.de/api/parties/1",
    #             "Sozialdemokratische Partei Deutschlands",
    #             "SPD",
    #             1,
    #         )
    #     ]
    #     # Cleanup
    #     session.execute(text("DELETE FROM party_style"))
    #     session.execute(text("DELETE FROM party"))

    # def test_prepare_update_data(self):
    #     # Arrange
    #     data = [
    #         {
    #             "id": 1,
    #             "entity_type": "party",
    #             "label": "SPD",
    #             "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
    #             "full_name": "Sozialdemokratische Partei Deutschlands",
    #             "short_name": "SPD",
    #         },
    #         {
    #             "id": 2,
    #             "entity_type": "party",
    #             "label": "CDU",
    #             "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
    #             "full_name": "Christlich Demokratische Union Deutschlands",
    #             "short_name": "CDU",
    #         },
    #     ]
    #     event = events.MissingEntityFetched(entity="party", data=data)
    #     # Act
    #     result = handlers.prepare_update_data(event)
    #     # Assert
    #     assert result == {
    #         "entities": ["party_style", "party"],
    #         "data": [
    #             [
    #                 {
    #                     "id": 1,
    #                     "display_name": "SPD",
    #                     "foreground_color": "#FFFFFF",
    #                     "background_color": "#333333",
    #                     "border_color": None,
    #                 },
    #                 {
    #                     "id": 2,
    #                     "display_name": "CDU",
    #                     "foreground_color": "#FFFFFF",
    #                     "background_color": "#333333",
    #                     "border_color": None,
    #                 },
    #             ],
    #             [
    #                 {
    #                     "id": 1,
    #                     "entity_type": "party",
    #                     "label": "SPD",
    #                     "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
    #                     "full_name": "Sozialdemokratische Partei Deutschlands",
    #                     "short_name": "SPD",
    #                     "party_style_id": 1,
    #                 },
    #                 {
    #                     "id": 2,
    #                     "entity_type": "party",
    #                     "label": "CDU",
    #                     "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
    #                     "full_name": "Christlich Demokratische Union Deutschlands",
    #                     "short_name": "CDU",
    #                     "party_style_id": 2,
    #                 },
    #             ],
    #         ],
    #     }

    # def test_update_table(self, session):
    #     # Arrange
    #     entities = ["party_style", "party"]
    #     data = [
    #         [
    #             {
    #                 "id": 1,
    #                 "display_name": "SPD",
    #                 "foreground_color": "#000000",
    #                 "background_color": "#FFFFFF",
    #                 "border_color": "#000000",
    #             },
    #             {
    #                 "id": 2,
    #                 "display_name": "SPD",
    #                 "foreground_color": "#000000",
    #                 "background_color": "#FFFFFF",
    #                 "border_color": "#000000",
    #             },
    #         ],
    #         [
    #             {
    #                 "id": 1,
    #                 "entity_type": "party",
    #                 "label": "SPD",
    #                 "api_url": "https://www.abgeordnetenwatch.de/api/parties/1",
    #                 "full_name": "Sozialdemokratische Partei Deutschlands",
    #                 "short_name": "SPD",
    #                 "party_style_id": 1,
    #             },
    #             {
    #                 "id": 2,
    #                 "entity_type": "party",
    #                 "label": "CDU",
    #                 "api_url": "https://www.abgeordnetenwatch.de/api/parties/2",
    #                 "full_name": "Christlich Demokratische Union Deutschlands",
    #                 "short_name": "CDU",
    #                 "party_style_id": 2,
    #             },
    #         ],
    #     ]
    #     event = events.UpdatedEntityPrepared(
    #         entities=entities, data=data, session=session
    #     )
    #     # Act
    #     handlers.update_table(event)
    #     rows = session.execute(
    #         text("SELECT * FROM party_style WHERE id = :id"), {"id": 1}
    #     )
    #     # Assert
    #     assert list(rows) == [
    #         (
    #             1,
    #             "SPD",
    #             "#000000",
    #             "#FFFFFF",
    #             "#000000",
    #         )
    #     ]
    #     # Act
    #     rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 1})
    #     # Assert
    #     assert list(rows) == [
    #         (
    #             1,
    #             "party",
    #             "SPD",
    #             "https://www.abgeordnetenwatch.de/api/parties/1",
    #             "Sozialdemokratische Partei Deutschlands",
    #             "SPD",
    #             1,
    #         )
    #     ]
    #     # Cleanup
    #     session.execute(text("DELETE FROM party_style"))
    #     session.execute(text("DELETE FROM party"))

    # def test_fetch_missing_party_update_table(self, session):
    #     factory = repository.SqlAlchemyFactory(session)
    #     repo = factory.create_party_repository()
    #     missing_party_data = utils.FetchMissingEntity(
    #         "parties", repo
    #     ).fetch_missing_entities()
    #     update_data = messagebus.handle(
    #         events.MissingEntityFetched(entity="party", data=missing_party_data)  # type: ignore
    #     )
    #     messagebus.handle(
    #         events.UpdatedEntityPrepared(
    #             **update_data[0], session=session  # type: ignore
    #         )
    #     )  # type: ignore
    #     rows = session.execute(
    #         text("SELECT * FROM party_style WHERE id = :id"), {"id": 1}
    #     )
    #     # Assert
    #     assert list(rows) == [(1, "SPD", "#000000", "#FFFFFF", "#000000")]
    #     # Act
    #     rows = session.execute(text("SELECT * FROM party WHERE id = :id"), {"id": 1})
    #     # # Assert
    #     assert list(rows) == [
    #         (
    #             1,
    #             "party",
    #             "SPD",
    #             "https://www.abgeordnetenwatch.de/api/parties/1",
    #             "Sozialdemokratische Partei Deutschlands",
    #             "SPD",
    #             1,
    #         )
    #     ]
    #     # Cleanup
    #     session.execute(text("DELETE FROM party_style"))
    #     session.execute(text("DELETE FROM party"))
