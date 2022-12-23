from fastapi import Response
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from .deps import get_context
from .management import Query

router = APIRouter()

graphql_router = GraphQLRouter(
    Schema(Query),
    graphiql=True,
    context_getter=get_context,
)

router.include_router(graphql_router, prefix="/graphql")


@router.get("/")
async def default() -> Response:
    return RedirectResponse(url="/graphql")
