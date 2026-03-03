from fastapi import FastAPI
from typing import Optional, Sequence, AsyncIterator
from contextlib import asynccontextmanager
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from starlette.middleware.cors import CORSMiddleware

from api.routes import router_hh
from producers.reaction_producer import rabbitmq_client


async def startup() -> None:
    try:
        await rabbitmq_client.connect()
    except Exception as exp:
        pass


async def shutdown() -> None:
    # можно сделать отмену фоновых задач, закрытие соединений и т.п.
    await rabbitmq_client.close()


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

    service.include_router(router_hh)

    service.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # Allow cookies, authorization headers, etc.
        allow_methods=["*"],  # Allow all standard HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    return service
