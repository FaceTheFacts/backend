from fastapi import HTTPException


def check_entity_not_found(entity, stringified_entity: str):
    if entity is None:
        raise HTTPException(status_code=404, detail=f"{stringified_entity} not found")
