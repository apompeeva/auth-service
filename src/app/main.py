from fastapi import FastAPI
from src.app.endpoints.endpoints import auth_router


app = FastAPI()

app.include_router(auth_router, tags=["auth"])
