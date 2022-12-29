from sqlalchemy import func, cast, ARRAY, String
from sqlalchemy.dialects.postgresql import aggregate_order_by, array
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session, aliased

from ...db import TradeEntity, AssetEntity, FeeEntity, LabelValueEntity, LabelKeyEntity


def query_trades(
            session: Session,
            base_asset_symbol: str = None,
            cursor: str = None,
            limit: int = 11
        ) -> tuple[list[Row], int]:
    base = aliased(AssetEntity)
    quote = aliased(AssetEntity)
    currency = aliased(AssetEntity)

    query = session.query(
            TradeEntity.id_.label('trade_id'),
            base.symbol.label('base_symbol'),
            TradeEntity.amount.label('trade_amount'),
            quote.symbol.label('quote_symbol'),
            TradeEntity.price.label('trade_price'),
            FeeEntity.amount.label('fee_amount'),
            currency.symbol.label('fee_currency'),
            TradeEntity.placed_at.label('trade_placed_at'),
            func.array_agg(array([LabelValueEntity.value, LabelKeyEntity.name])).label('trade_labels'),
        )\
        .join(base, base.id_ == TradeEntity.base_id)\
        .join(quote, quote.id_ == TradeEntity.quote_id)\
        .join(FeeEntity, FeeEntity.id_ == TradeEntity.fee_id)\
        .join(currency, currency.id_ == FeeEntity.currency_id) \
        .outerjoin(LabelValueEntity, LabelValueEntity.trade_id == TradeEntity.id_) \
        .outerjoin(LabelKeyEntity, LabelKeyEntity.id_ == LabelValueEntity.key_id) \
        .order_by(TradeEntity.id_.desc())\
        .group_by(
            TradeEntity.id_,
            base.symbol,
            TradeEntity.amount,
            quote.symbol,
            TradeEntity.price,
            FeeEntity.amount,
            currency.symbol,
            TradeEntity.placed_at,
        )

    if base_asset_symbol:
        query = query.filter(base.symbol == base_asset_symbol)

    if cursor:
        query = query.filter(TradeEntity.id_ < cursor)
    return query.limit(limit), query.count()
