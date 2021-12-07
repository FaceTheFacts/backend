from typing import Dict, List


class ProfileUrl:
    profile_url: Dict[str, str]


class ScrapedWeblink:
    id: Dict[str, str]
    weblink: Dict[str, List[str]]


class ProcessedWeblink:
    politician_id: Dict[str, int]
    weblink: Dict[str, List[str]]
