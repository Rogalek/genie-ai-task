import uuid

from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from . import Base


class LabelKeyEntity(Base):
    __tablename__ = "label_key"

    id_ = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column("name", VARCHAR(), nullable=False, unique=True)


class LabelValueEntity(Base):
    __tablename__ = "label_value"

    id_: uuid.UUID = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    key_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("label_key.id"), nullable=False)
    key: LabelKeyEntity = relationship(LabelKeyEntity, foreign_keys=[key_id], lazy="select")

    value: str = Column("value", VARCHAR(), nullable=True)

    trade_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("trade.id"), nullable=False)
