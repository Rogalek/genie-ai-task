import strawberry
import typing

from ...deps import GenieInfo
from .database import query_trades


@strawberry.type
class Trade:
    id: str
    base_asset_symbol: str
    amount: str
    quote_asset_symbol: str
    price: str
    fee: str
    fee_currency: str
    placed_at: str
    labels: typing.List[typing.Tuple[str, str]]


async def get_trades(
            base_asset_symbol: typing.Optional[str] = None,
            cursor: str = None,
            limit: int = 11,
            info: GenieInfo = None
        ) -> typing.Tuple[list[Trade], int]:
    with info.context.session_factory.begin() as session:
        rows, count = query_trades(session, base_asset_symbol, cursor, limit)
        return [Trade(
            id=row.trade_id,
            base_asset_symbol=row.base_symbol,
            amount=row.trade_amount,
            quote_asset_symbol=row.quote_symbol,
            price=row.trade_price,
            fee=row.fee_amount,
            fee_currency=row.fee_currency,
            placed_at=row.trade_placed_at,
            labels=row.trade_labels,
        ) for row in rows], count
