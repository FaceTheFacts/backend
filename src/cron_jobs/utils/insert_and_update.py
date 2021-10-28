from typing import Any
from sqlalchemy.dialects.postgresql import insert
from src.db.connection import Session


def insert_and_update(model: Any, data: list[Any]) -> None:
    session = Session()
    stmt = insert(model).values(data)
    stmt = stmt.on_conflict_do_update(
        constraint=f"{model.__tablename__}_pkey",
        set_={col.name: col for col in stmt.excluded if not col.primary_key},
    )
    session.execute(stmt)
    session.commit()
    session.close()
