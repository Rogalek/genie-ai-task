from typing import NewType

import arrow
import strawberry

ArrowType = strawberry.scalar(NewType("ArrowType", arrow.Arrow), serialize=str, parse_value=arrow.get)
