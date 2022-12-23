import random
from decimal import Decimal

import arrow
import uvicorn
from sqlalchemy import DDL

from .db import AssetEntity, Base, FeeEntity, LabelKeyEntity, LabelValueEntity, TradeEntity, UserEntity
from .deps import get_engine, get_session_factory


def recreate_tables():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(DDL(f"CREATE SCHEMA IF NOT EXISTS {Base.metadata.schema}"))
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

    engine.dispose()


def insert_data():
    engine = get_engine()
    random.seed(0)
    with get_session_factory().begin() as session:
        test_user = UserEntity(username="test_user")
        session.add(test_user)

        quote = AssetEntity(symbol="USDT", name="Tether")
        session.add(quote)

        fee_currency = AssetEntity(symbol="BNB", name="Binance Coin")
        session.add(fee_currency)

        base_assets = [
            AssetEntity(symbol="BTC", name="Bitcoin"),
            AssetEntity(symbol="ETH", name="Ethereum"),
            AssetEntity(symbol="DOGE", name="Dogecoin"),
            AssetEntity(symbol="MATIC", name="Polygon"),
            AssetEntity(symbol="DOT", name="Polkadot"),
            AssetEntity(symbol="ATOM", name="Cosmos"),
        ]
        session.add_all(base_assets)

        sector_key = LabelKeyEntity(name="strategy")
        session.add(sector_key)
        risk_key = LabelKeyEntity(name="risk")
        session.add(risk_key)

        strategy_values = ["speculate", "buy_and_hold"]
        risk_values = ["high", "moderate", "low"]

        fee_sample = [Decimal("0.25"), Decimal("0.5"), Decimal("0.75"), Decimal("1.0")]
        start_time = arrow.Arrow(2020, 1, 1)  # noqa: WPS432
        for _ in range(1000):
            fee = FeeEntity(currency=fee_currency, amount=random.choice(fee_sample))
            session.add(fee)
            base = random.choice(base_assets)
            price = Decimal(str(round(random.uniform(1.0, 100.0), 4)))
            amount = Decimal(str(round(random.uniform(1.0, 100.0), 4)))
            placed_at = start_time.shift(days=random.randint(0, 1000))
            strategy = LabelValueEntity(key=sector_key, value=random.choice(strategy_values))
            risk = LabelValueEntity(key=risk_key, value=random.choice(risk_values))
            trade = TradeEntity(
                price=price,
                amount=amount,
                base=base,
                quote=quote,
                fee=fee,
                user=test_user,
                placed_at=placed_at,
                labels=[risk, strategy],
            )
            session.add(trade)

    engine.dispose()


recreate_tables()
insert_data()
uvicorn.run("home_assignment.app:get_app", reload=True, host="localhost", port=8080)  # noqa: WPS432
