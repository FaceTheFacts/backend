from unittest import TestCase, mock

from src.api.utils.politician import _shorten_occupation, get_occupations


@mock.patch.dict(
    "src.api.utils.politician.OCCUPATIONS",
    {
        1: ["job1", "job2"],
        2: ["some_other_job"],
        3: ["job3", "some_other_job"],
    },
)
@mock.patch(
    "src.api.utils.politician._split_map_occupation",
    return_value=["val1", "val2", "val3"],
)
class TestGetOccupations(TestCase):
    def test_custom_occupation(self, mock):
        expected = ["job3", "some_other_job"]
        actual = get_occupations("soihoi299fnlad", 3)
        self.assertEqual(expected, actual)

    def test_unknown_occupation(self, mock):
        expected = ["val1", "val2", "val3"]
        actual = get_occupations("unknown", 7)
        self.assertEqual(expected, actual)

    def test_no_occupation(self, mock):
        expected = []
        actual = get_occupations(None, 9)
        self.assertEqual(expected, actual)


class TestShortenOccupation(TestCase):
    def test_fully_known_occupations(self):
        known_items = [
            ("Bundesminister des Auswärtigen", "Außenminister"),
            (
                "Bundesministerin für Umwelt, Naturschutz und nukleare Sicherheit",
                "Bundesumweltministerin",
            ),
            (
                "Bundesminister für wirtschaftliche Zusammenarbeit und Entwicklung",
                "Bundesentwicklungshilfeminister",
            ),
        ]
        for item in known_items:
            self.assertEqual(item[1], _shorten_occupation(item[0]))

    def test_known_substring(self):
        test_items = [
            (
                "random text Fraktionsvorsitzender more random text",
                "Fraktionsvorsitzender",
            ),
            ("some more text Landesgruppenchef random other text", "Landesgruppenchef"),
            (
                "kjsdlaRegierender Bürgermeisterhgopjasdmsddsa",
                "Regierender Bürgermeister",
            ),
            (
                "ihosdheoioawBundesvorsitzenderjjhdosjapwjowjdksngior",
                "Bundesvorsitzender",
            ),
        ]
        for item in test_items:
            self.assertEqual(item[1], _shorten_occupation(item[0]))

    def test_unknown_item(self):
        test_items = [
            "klhgjsponsdiownfsfkdpa",
            "opjwopfdng[bs;gsdgs",
            "piwbnbmf.boia6787osfnasf",
        ]

        for item in test_items:
            self.assertEqual(item, _shorten_occupation(item))
