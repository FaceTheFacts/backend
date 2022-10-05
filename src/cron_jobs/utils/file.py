# std
from typing import Any, List
import os.path as path
import json
import time


def has_valid_file(file_path: str) -> bool:
    has_file = path.isfile(file_path)

    # Check if file is a day old
    if has_file and (time.time() - path.getatime(file_path)) / 3600 < 24:
        return True
    return False


def read_json(file_path: str) -> Any:
    with open(file_path, encoding="utf8") as read_file:
        data = json.load(read_file)
        print(f"Loaded data from {file_path}")
        return data


def write_json(file_path: str, data: List[Any]) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
