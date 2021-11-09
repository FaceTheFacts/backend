from src.api.utils.sidejob import convert_income_level


def test_convert_income_level():
    assert convert_income_level("1") == "1.000 € bis 3.500 €"
    assert convert_income_level("3") == "7.000 € bis 15.000 €"
    assert convert_income_level("10") == "ab 250.000 €"
    assert convert_income_level(None) == None
