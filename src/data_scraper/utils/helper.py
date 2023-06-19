# Default
import json


def fetch_json(file_name: str) -> any:
    BASE_PATH = "src/json/"
    selected_path = BASE_PATH + file_name + ".json"
    with open(selected_path) as read_file:
        data = json.load(read_file)
    return data


def generate_json(data: list, file_name: str) -> None:
    with open(
        "src/json/{name}.json".format(name=file_name), "w", encoding="utf-8"
    ) as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
