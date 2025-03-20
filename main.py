from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.user.router import user_router
from app.config import settings
from app.core.database.service import DBService
from app.core.database.utils import DBUtils


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.create_tables()
    yield
    await DBService.drop_tables()  # TODO turn off
    await DBUtils.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
