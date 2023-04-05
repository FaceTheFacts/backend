from unittest.mock import MagicMock
import pytest
from src.api.utils.speeches import (
    clean_text,
    is_politician_comment,
    extract_comment,
    extract_politician_name,
    process_speech_data,
)


def test_clean_text():
    assert clean_text("This is a normal string") == "This is a normal string"
    assert (
        clean_text("This is a string with a non-printable character\x80")
        == "This is a string with a non-printable character "
    )
    assert (
        clean_text("\tThis is a string with a tab") == "\tThis is a string with a tab"
    )
    assert (
        clean_text("This is a\x80string with\x81multiple non-printable\x82characters")
        == "This is a string with multiple non-printable characters"
    )
    assert (
        clean_text("\x80This\x81 is a string \x82with a mix of characters")
        == " This  is a string  with a mix of characters"
    )


def test_is_politician_comment():
    assert is_politician_comment("(Dr. John Doe [SPD]: This is a comment)") == True
    assert is_politician_comment("(Jane Doe [CDU/CSU]: Another comment)") == True
    assert is_politician_comment("This is not a comment") == False
    assert is_politician_comment("(John Doe: This is a comment)") == True
    assert is_politician_comment("(Dr. Jane Smith: Another comment)") == True
    assert is_politician_comment("(Alice Johnson [GRÜNE]: Yet another comment)") == True


def test_extract_comment():
    assert (
        extract_comment("(Dr. John Doe [SPD]: This is a comment)")
        == "This is a comment"
    )
    assert extract_comment("(Jane Doe [CDU/CSU]: Another comment)") == "Another comment"
    assert extract_comment("(John Doe: This is a comment)") == "This is a comment"
    assert extract_comment("(Dr. Jane Smith: Another comment)") == "Another comment"
    assert (
        extract_comment("(Alice Johnson [GRÜNE]: Yet another comment)")
        == "Yet another comment"
    )


def test_extract_politician_name():
    assert (
        extract_politician_name("(Dr. John Doe [SPD]: This is a comment)") == "John Doe"
    )
    assert extract_politician_name("(Jane Doe [CDU/CSU]: Another comment)")
    assert extract_politician_name("(John Doe: This is a comment)") == "John Doe"
    assert extract_politician_name("(Dr. Jane Smith: Another comment)") == "Jane Smith"
    assert (
        extract_politician_name("(Alice Johnson [GRÜNE]: Yet another comment)")
        == "Alice Johnson"
    )


def generate_raw_data_single_speech():
    return {
        "data": [
            {
                "attributes": {
                    "videoFileURI": "url_1",
                    "dateStart": "2022-01-01",
                    "textContents": [],
                },
                "annotations": {
                    "data": [
                        {
                            "attributes": {
                                "additionalInformation": {"role": "Abgeordnete"}
                            }
                        }
                    ]
                },
                "relationships": {
                    "people": {
                        "data": [
                            {
                                "attributes": {
                                    "additionalInformation": {
                                        "abgeordnetenwatchID": 119742
                                    }
                                }
                            }
                        ]
                    },
                    "agendaItem": {"data": {"attributes": {"title": "title_1"}}},
                },
            }
        ],
        "meta": {"results": {"count": 1, "total": 1}},
    }


def generate_raw_data_multiple_speeches():
    return {
        "data": [
            {
                "id": "DE-1",
                "attributes": {
                    "videoFileURI": "url_1",
                    "dateStart": "2022-01-01",
                    "textContents": [
                        {
                            "textBody": [
                                {
                                    "type": "speech",
                                    "sentences": [
                                        {
                                            "timeStart": 0,
                                            "timeEnd": 10,
                                            "text": "This is a comment",
                                        }
                                    ],
                                },
                                {
                                    "type": "comment",
                                    "sentences": [
                                        {
                                            "timeStart": 0,
                                            "timeEnd": 10,
                                            "text": "This is another comment",
                                        }
                                    ],
                                },
                            ]
                        }
                    ],
                },
                "annotations": {
                    "data": [
                        {
                            "attributes": {
                                "additionalInformation": {"role": "Abgeordnete"}
                            }
                        }
                    ]
                },
                "relationships": {
                    "people": {
                        "data": [
                            {
                                "attributes": {
                                    "additionalInformation": {
                                        "abgeordnetenwatchID": 119742
                                    }
                                }
                            }
                        ]
                    },
                    "agendaItem": {"data": {"attributes": {"title": "title_1"}}},
                    "session": {"data": {"id": "1"}},
                    "electoralPeriod": {"data": {"attributes": {"number": 19}}},
                },
            },
        ],
        "meta": {"results": {"count": 2, "total": 2}},
    }


def test_process_speech_data_single_speech_abgeordnetenwatch_id():
    raw_data = generate_raw_data_single_speech()
    get_entity_by_id_func = MagicMock()
    get_politician_with_mandate_by_name_func = MagicMock()

    actual = process_speech_data(
        db=None,
        get_entity_by_id_func=get_entity_by_id_func,
        get_politician_with_mandate_by_name_func=get_politician_with_mandate_by_name_func,
        page=1,
        raw_data=raw_data,
        abgeordnetenwatch_id=119742,
    )
    expected = {
        "items": [
            {
                "videoFileURI": "url_1",
                "title": "title_1",
                "date": "2022-01-01",
            },
        ],
        "total": 1,
        "page": 1,
        "size": 1,
        "politician_id": 119742,
        "is_last_page": True,
    }
    assert actual == expected


def test_process_speech_data_multiple_speeches_no_abgeordnetenwatch_id():
    raw_data = generate_raw_data_multiple_speeches()
    get_entity_by_id_func = MagicMock()
    get_politician_with_mandate_by_name_func = MagicMock()

    get_entity_by_id_func.return_value = MagicMock(id=119742)

    actual = process_speech_data(
        db=None,
        get_entity_by_id_func=get_entity_by_id_func,
        get_politician_with_mandate_by_name_func=get_politician_with_mandate_by_name_func,
        page=1,
        raw_data=raw_data,
    )
    expected = {
        "items": [
            {
                "date": "2022-01-01",
                "id": "1",
                "parliament_period_id": 111,
                "politician_id": 119742,
                "session": "1",
                "text": [{"end": 10, "start": 0, "text": ["This is a comment"]}],
                "title": "title_1",
                "videoFileURI": "url_1",
            }
        ],
        "total": 2,
        "page": 1,
        "size": 1,
        "is_last_page": True,
    }
    assert actual == expected
