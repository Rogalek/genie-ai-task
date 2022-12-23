from datetime import datetime
from typing import Iterable

import arrow
from sqlalchemy import TypeDecorator
from sqlalchemy.sql import sqltypes


class DecimalType(sqltypes.Numeric):
    def __init__(self):
        super().__init__(precision=16, scale=8)  # noqa: WPS432


class ArrowType(TypeDecorator):
    impl = sqltypes.DateTime
    cache_ok = True

    def __init__(self, timezone: bool = True):
        super().__init__(timezone=timezone)

    def process_bind_param(self, value, dialect):
        if value:
            utc_val = self._coerce(value).to("UTC")
            if self.impl.timezone:
                return utc_val.datetime
            return utc_val.naive
        return value

    def process_result_value(self, value, dialect):
        if value:
            return arrow.get(value)
        return value

    def process_literal_param(self, value, dialect):
        return str(value)

    @property
    def python_type(self):
        return self.impl.python_type

    def _coerce(self, value):
        if isinstance(value, str):
            value = arrow.get(value)
        elif isinstance(value, Iterable):
            value = arrow.get(*value)
        elif isinstance(value, datetime):
            value = arrow.get(value)

        return value
