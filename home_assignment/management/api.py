import strawberry

from .asset import get_assets
from .user import get_users


@strawberry.type
class Management:
    users = strawberry.field(resolver=get_users)
    assets = strawberry.field(resolver=get_assets)


@strawberry.type
class Query:
    management: Management = strawberry.field(resolver=Management)
