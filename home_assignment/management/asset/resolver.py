import strawberry

from ...deps import GenieInfo
from .database import query_assets


@strawberry.type
class Asset:
    symbol: str
    name: str


async def get_assets(info: GenieInfo) -> list[Asset]:
    with info.context.session_factory.begin() as session:
        assets = query_assets(session)
        return [Asset(symbol=asset.symbol, name=asset.name) for asset in assets]
