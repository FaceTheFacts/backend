import urllib.request
from urllib.error import HTTPError
from typing import List, Optional, Dict

from src.api.utils.exceptions import OCCUPATIONS
from src.db import models


def add_image_urls_to_politicians(politicians: List[models.Politician]):
    for politician in politicians:
        image_url = f"https://candidate-images.s3.eu-central-1.amazonaws.com/{politician.id}.jpg"

        try:
            urllib.request.urlopen(image_url)
            politician.__dict__["image_url"] = image_url
        except HTTPError:
            politician.__dict__["image_url"] = None

    return politicians


def get_occupations(occupation: Optional[str], politician_id: int) -> List[str]:
    # if we have a custom occupation, we take it
    if (custom_occupation := OCCUPATIONS.get(politician_id)) is not None:
        return custom_occupation
    # if there is no occupation, we return an empty list
    elif occupation == None:
        return []
    # else we process the occupation string from AW
    else:
        return _split_map_occupation(occupation)


def _split_map_occupation(occupation: str) -> List[str]:
    # this replace needs to happen before splitting, since it contains a ','
    occupation = occupation.replace(
        "Bundesministerin für Umwelt, Naturschutz und nukleare Sicherheit",
        "Bundesumweltministerin",
    )

    # limit to 3 results
    split = occupation.split(",")
    if len(split) > 3:
        split = split[:3]

    return [_shorten_occupation(i.strip()) for i in split]


def _shorten_occupation(o: str):
    """
    Replace long titles with short forms.
    # warning
    For male and female versions of one word, watch out to always match the longer one first!
    """
    # Fractions
    if o.find("Fraktionsvorsitzender") != -1:
        return "Fraktionsvorsitzender"
    elif o.find("Fraktionsvorsitzende") != -1:
        return "Fraktionsvorsitzende"
    elif o.find("Landesgruppenchefin") != -1:
        return "Landesgruppenchefin"
    elif o.find("Landesgruppenchef") != -1:
        return "Landesgruppenchef"

    # Ministries
    elif o == "Bundesminister des Auswärtigen":
        return "Außenminister"
    elif o == "Bundesminister für Wirtschaft und Energie":
        return "Bundeswirtschaftsminister"
    elif o == "Bundesministerin für Justiz und Verbraucherschutz":
        return "Bundesjustizministerin"
    elif o == "Bundesminister für Arbeit und Soziales":
        return "Bundesarbeitsminister"
    elif o == "Bundesminister für Gesundheit":
        return "Bundesgesundheitsminister"
    elif o == "Bundesminister für Verkehr und digitale Infrastruktur":
        return "Bundesverkehrsminister"
    elif o == "Bundesministerin für Umwelt, Naturschutz und nukleare Sicherheit":
        return "Bundesumweltministerin"
    elif o == "Bundesministerin für Bildung und Forschung":
        return "Bundesbildungsministerin"
    elif o == "Bundesminister für wirtschaftliche Zusammenarbeit und Entwicklung":
        return "Bundesentwicklungshilfeminister"
    elif o == "Bundesminister für besondere Aufgaben und Chef des Bundeskanzleramts":
        return "Chef des Bundeskanzleramts"

    # Head of government
    elif o.find("Ministerpräsidentin") != -1:
        return "Ministerpräsidentin"
    elif o.find("Ministerpräsident") != -1:
        return "Ministerpräsident"
    elif o.find("Regierender Bürgermeister") != -1:
        return "Regierender Bürgermeister"
    elif o.find("Regierende Bürgermeisterin") != -1:
        return "Regierende Bürgermeisterin"

    # Party offices
    elif o.find("Bundesvorsitzender") != -1:
        return "Bundesvorsitzender"
    elif o.find("Bundesvorsitzende") != -1:
        return "Bundesvorsitzende"

    # ---
    else:
        return o


# Converts a list of items containing "id" and "parent_id" to a single list of id's
# If an item in the dict has a parent_id, return the parent_id to the list, instead of the item's id.
def transform_topics_dict_to_minimal_array(data: List[Dict[str, int or None]]) -> List:
    data_list = []
    if data:
        for item in data:
            id = item["id"]
            parent_id = item["parent_id"]

            if parent_id:
                if parent_id not in data_list:
                    data_list.append(parent_id)
                else:
                    continue

            if id not in data_list:
                data_list.append(id)

    return data_list
