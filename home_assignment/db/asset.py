import uuid

from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Column

from . import Base


class AssetEntity(Base):
    __tablename__ = "asset"

    id_: uuid.UUID = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: str = Column(VARCHAR(8), nullable=False)
    name: str = Column(VARCHAR(16), nullable=False)  # noqa: WPS432
