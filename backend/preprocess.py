# std
from typing import List, Optional

# local
from . import sort
from .types import Mandate
from data.occupations import OCCUPATIONS

def occupation(occupation: Optional[str], politician_id: int) -> list[str]:
    # if we have a custom occupation, we take it
    if (custom_occupation := OCCUPATIONS.get(politician_id)) != None:
        return custom_occupation
    # if there is no occupation, we return an empty list
    elif occupation == None:
        return []
    # else we process the occupation string from AW
    else:
        return _split_map_occupation(occupation)


def _split_map_occupation(occupation: str) -> list[str]:
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
    # elif o == "Bundesministerin für Umwelt, Naturschutz und nukleare Sicherheit":
    #     return "Bundesumweltministerin"
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


def party(party: str) -> str:
    if party == "Bündnis 90/Die Grünen":
        return "Die Grünen"
    else:
        return party


def second_vote(mandates: List[Mandate]) -> List[Mandate]:
    filtered_mandates = list(
        filter(lambda x: x["electoral_data"]["list_position"] != None, mandates)
    )
    return sort.second_vote(filtered_mandates)


def first_vote(mandates: List[Mandate]) -> List[Mandate]:
    cleaned_first_vote = list()
    for mandate in mandates:
        mandate["party"]["label"] = party(mandate["party"]["label"])
        cleaned_first_vote.append(mandate)
    return cleaned_first_vote
