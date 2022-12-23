import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from home_assignment.deps import get_engine
from home_assignment.router import router
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def get_local_app(engine: Engine) -> FastAPI:
    local_app = FastAPI(
        title="assignment",
        default_response_class=UJSONResponse,
    )

    @local_app.on_event("shutdown")
    def dispose_db_engine() -> None:
        logger.debug("Disposing the database engine")
        engine.dispose()

    local_app.include_router(router=router)

    return local_app


def get_app() -> FastAPI:
    engine = get_engine()
    return get_local_app(engine)
