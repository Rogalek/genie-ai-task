import base64
from typing import TypeVar, Generic, List, Optional

import strawberry
from strawberry import UNSET

from .asset import get_assets
from .trades.resolver import Trade
from .user import get_users
from .trades import get_trades
from ..deps import GenieInfo

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    page_info: "PageInfo"
    edges: List["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    has_previous_page: bool
    has_next_page: bool
    count: int
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType
    cursor: str


def build_trade_cursor(trade: Trade):
    trade_id = f"{trade.id}".encode("utf-8")
    return base64.b64encode(trade_id).decode()


async def _get_trades(
            first: int = 10,
            after: Optional[str] = UNSET,
            base_asset_symbol: Optional[str] = None,
            info: GenieInfo = None
        ) -> Connection[Trade]:
    """"""
    after = base64.b64decode(after).decode() if after is not UNSET else None
    trades, count = await get_trades(base_asset_symbol, after, first + 1, info)
    has_next_page = len(trades) > first

    edges = [
        Edge(node=trade, cursor=build_trade_cursor(trade))
        for trade in trades[:-1]
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=False,
            has_next_page=has_next_page,
            count=count,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if len(edges) > 1 else None,
        ),
        edges=edges
    )


@strawberry.type
class Management:
    users = strawberry.field(resolver=get_users)
    assets = strawberry.field(resolver=get_assets)


@strawberry.type
class Query:
    management: Management = strawberry.field(resolver=Management)
    trades = strawberry.field(resolver=_get_trades)
