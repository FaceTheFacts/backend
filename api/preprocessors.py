def preprocess_occupation(occupation: str) -> list[str]:
    return [i.strip() for i in occupation.split(",")]


def preprocess_party(party: str) -> str:
    return party
