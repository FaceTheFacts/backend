from src.api.security import get_cors_allowed_origins


def test_get_cors_allowed_origins_defaults_to_empty(monkeypatch):
    monkeypatch.delenv("CORS_ALLOWED_ORIGINS", raising=False)

    assert get_cors_allowed_origins() == []


def test_get_cors_allowed_origins_parses_csv(monkeypatch):
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "https://facethefacts.app, http://localhost:19006, ,https://test.example",
    )

    assert get_cors_allowed_origins() == [
        "https://facethefacts.app",
        "http://localhost:19006",
        "https://test.example",
    ]
