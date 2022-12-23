import uuid
from decimal import Decimal

from arrow import Arrow
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from . import ArrowType, AssetEntity, Base, DecimalType, FeeEntity, LabelValueEntity, UserEntity


class TradeEntity(Base):
    __tablename__ = "trade"

    id_ = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    base_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    base: AssetEntity = relationship(AssetEntity, foreign_keys=[base_id], lazy="select")

    quote_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    quote: AssetEntity = relationship(AssetEntity, foreign_keys=[quote_id], lazy="select")

    fee_id = Column(UUID(as_uuid=True), ForeignKey("fee.id"))
    fee: FeeEntity = relationship(FeeEntity, foreign_keys=[fee_id], lazy="select")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user: UserEntity = relationship(UserEntity, foreign_keys=[user_id], lazy="select")

    labels: list[LabelValueEntity] = relationship(LabelValueEntity)

    amount: Decimal = Column(DecimalType())
    price: Decimal = Column(DecimalType())
    placed_at: Arrow = Column(ArrowType())
