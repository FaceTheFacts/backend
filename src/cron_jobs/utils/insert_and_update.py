# std
from typing import Any, List

# local
from src.db.connection import Session

# third-party
from sqlalchemy.dialects.postgresql import insert


def insert_and_update(model: Any, data: List[Any]) -> None:
    session = Session()
    stmt = insert(model).values(data)
    stmt = stmt.on_conflict_do_update(
        constraint=f"{model.__tablename__}_pkey",
        set_={col.name: col for col in stmt.excluded if not col.primary_key},
    )
    session.execute(stmt)
    session.commit()
    session.close()


def insert_only(model: Any, data: List[Any]) -> None:
    session = Session()
    stmt = insert(model).values(data)
    session.execute(stmt)
    session.commit()
    session.close()
