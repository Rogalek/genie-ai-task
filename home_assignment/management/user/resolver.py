import arrow
import strawberry

from ...deps import GenieInfo
from ..scalars import ArrowType
from .database import query_users


@strawberry.type
class User:
    name: str
    created_at: ArrowType


async def get_users(info: GenieInfo) -> list[User]:
    with info.context.session_factory.begin() as session:
        users = query_users(session)
        return [User(name=user.username, created_at=arrow.utcnow()) for user in users]
