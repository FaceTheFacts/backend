# Default
import sys


sys.path.append("src")

# Default
from typing import List

# Third Party
import pandas
from pandas.core.frame import DataFrame

# Local
from utils.helper import fetch_json, generate_json
from utils.types import ProcessedWeblink, ProfileUrl, ScrapedWeblink


def generate_politician_df() -> DataFrame:
    # csv from politician table
    df = pandas.read_csv(
        "src/utils/politician_id_url.csv",
        encoding="utf8",
        names=["id", "profile_url"],
    )
    return df


def generate_politician_url() -> List[ProfileUrl]:
    df = generate_politician_df()
    return df["profile_url"].values.tolist()


def remove_empty_weblinks() -> List[ScrapedWeblink]:
    data_list = []
    profile = fetch_json("profile")
    for item in profile:
        is_empty_weblinks = len(item["weblink"]) == 0
        if is_empty_weblinks != True:
            data_list.append(item)
    return data_list


def get_id_from_link(item: dict) -> int:
    # e.g., id = ["/open-data/info/politician/178142/candidacy_mandate]"->
    # e.g., -> ['', 'open-data', 'info', 'politician', '178144', 'candidacy_mandate'] => 4th is politician_id
    id = int(item["id"][0].split("/")[4])
    return id


def generate_weblink_list() -> List[ProcessedWeblink]:
    data_list = []
    data = remove_empty_weblinks()
    for item in data:
        id = get_id_from_link(item)
        new_dict = {"politician_id": id, "weblink": item["weblink"]}
        data_list.append(new_dict)

    return data_list


def generate_weblink_json() -> None:
    data_list = generate_weblink_list()
    generate_json(data_list, "weblinks")


if __name__ == "__main__":
    generate_weblink_json()
