from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from opensearch.client import ensure_index
from routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # 起動時にOpenSearchのインデックスを作成
    ensure_index()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
