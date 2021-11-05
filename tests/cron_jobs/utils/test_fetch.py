from src.cron_jobs.utils.fetch import fetch_entity_count


def test_fetch_entity_count() -> int:
    assert fetch_entity_count("cities") == 1065
