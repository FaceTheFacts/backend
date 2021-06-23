import pytest

from api.preprocessors import preprocess_occupation, preprocess_party


@pytest.mark.parametrize(
    "input,expected",
    [
        # Analena Baerbock (79475)
        ("MdB, Bundesvorsitzende der Grünen", ["MdB", "Bundesvorsitzende"]),
        # Annegret Kramp-Karrenbauer (138124)
        ("Ministerpräsidentin des Saarlandes, MdL", ["MdL", "Ministerpräsidentin"]),
        # Hubertus Heil (79316)
        (
            "Bundesminister für Arbeit und Soziales, MdB, stellvertretender Fraktionsvorsitzender",
            ["MdB", "Bundesarbeitsminister", "Fraktionsvorsitzender"],
        ),
    ],
)
def test_preprocess_occupation(input: str, expected: list[str]):
    # `.sort` makes sure we don't care for the order of the result
    assert preprocess_occupation(input).sort() == expected.sort()


@pytest.mark.parametrize(
    "input,expected",
    [
        ("CDU", "CDU"),
        ("Bündnis 90/Die Grünen", "Die Grünen"),
        ("Die Linke", "Die Linke"),
        ("SPD", "SPD"),
    ],
)
def test_preprocess_party(input: str, expected: str):
    assert preprocess_party(input) == expected
