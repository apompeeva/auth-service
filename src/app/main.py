from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.endpoints.endpoints import auth_router
from app.producer.producer import producer
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await producer.start()
        yield
    except:
        yield
    finally:
        await producer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=['auth'])
