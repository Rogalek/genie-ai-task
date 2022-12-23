import uuid

from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Column

from .base import Base


class UserEntity(Base):
    __tablename__ = "user"

    id_ = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username: str = Column("username", VARCHAR(), nullable=False, unique=True)
