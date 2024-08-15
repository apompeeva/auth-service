from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.endpoints.endpoints import auth_router
from app.producer.producer import producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer.start()
    yield
    producer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=['auth'])
