import uuid
from decimal import Decimal

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from . import AssetEntity, Base, DecimalType


class FeeEntity(Base):
    __tablename__ = "fee"

    id_: uuid.UUID = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    currency_id = Column(UUID(as_uuid=True), ForeignKey("asset.id"))
    currency: AssetEntity = relationship(AssetEntity, foreign_keys=[currency_id], lazy="select")

    amount: Decimal = Column(DecimalType())
