import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.endpoints.endpoints import auth_router
from app.producer.producer import producer

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание продюсера перед запуском приложения и остановка после."""
    try:
        await producer.start()
        yield
    except:
        yield
    finally:
        await producer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=['auth'])
