from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from ...db import TradeEntity, AssetEntity


def query_trades(
            session: Session,
            base_asset_symbol: str = None,
            cursor: str = None,
            limit: int = 11
        ) -> tuple[list[Row], int]:
    query = session.query(TradeEntity)\
        .order_by(TradeEntity.id_.desc())
    if base_asset_symbol:
        query = query.join(AssetEntity, TradeEntity.base_id == AssetEntity.id_)\
            .filter(AssetEntity.symbol == base_asset_symbol)
    if cursor:
        query = query.filter(TradeEntity.id_ < cursor)
    return query.limit(limit), query.count()
