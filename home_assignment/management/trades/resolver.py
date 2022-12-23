import strawberry
import typing

from ...deps import GenieInfo
from .database import query_trades


@strawberry.type
class Trade:
    id: str
    base_asset_symbol: str
    amount: float
    quote_asset_symbol: str
    price: float
    fee: float
    fee_currency: str
    placed_at: str
    labels: typing.List[typing.Tuple[str, str]]


async def get_trades(
            base_asset_symbol: typing.Optional[str] = None,
            cursor: str = None,
            limit: int = 10,
            info: GenieInfo = None
        ) -> typing.Tuple[list[Trade], int]:
    with info.context.session_factory.begin() as session:
        trades, count = query_trades(session, base_asset_symbol, cursor, limit)
        return [Trade(
            id=trade.id_,
            base_asset_symbol=trade.base.symbol,
            amount=trade.amount,
            quote_asset_symbol=trade.quote.symbol,
            price=trade.price,
            fee=trade.fee.amount,
            fee_currency=trade.fee.currency.symbol,
            placed_at=trade.placed_at,
            labels=[(label.key.name, label.value) for label in trade.labels],
        ) for trade in trades], count
