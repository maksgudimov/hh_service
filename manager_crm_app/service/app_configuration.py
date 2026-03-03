from fastapi import FastAPI
from typing import Optional, Sequence, AsyncIterator
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from api.routes import router_auth, router_vacancies, router_reactions, router_notification_service
from consumers.reaction_consumer import consumer



async def startup() -> None:
    try:
        await consumer.run()
    except Exception as exp:
        pass


async def shutdown() -> None:
    # можно сделать отмену фоновых задач, закрытие соединений и т.п.
    await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await startup()
    yield
    await shutdown()


def create_service() -> FastAPI:
    service = FastAPI(
        docs_url="/inspection/docs",
        redoc_url="/inspection/redoc",
        openapi_url="/inspection/openapi.json",
        lifespan=lifespan
    )

    service.include_router(router_auth, prefix="/api/v1")
    service.include_router(router_vacancies, prefix="/api/v1")
    service.include_router(router_reactions, prefix="/api/v1")
    service.include_router(router_notification_service, prefix="/api/v1")

    service.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # Allow cookies, authorization headers, etc.
        allow_methods=["*"],  # Allow all standard HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    return service
