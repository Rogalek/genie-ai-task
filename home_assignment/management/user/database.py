from sqlalchemy import select
from sqlalchemy.orm import Session

from ...db import UserEntity


def query_users(session: Session) -> list[UserEntity]:
    results = session.execute(select(UserEntity))
    return results.scalars().fetchall()
