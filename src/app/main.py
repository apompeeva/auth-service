import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.endpoints.endpoints import auth_router
from app.producer.producer import producer
from prometheus_client import make_asgi_app
from app.metrics import REQUEST_COUNT, REQUEST_DURATION

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

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)


@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if request.url.path in ['/auth', '/register', '/api/verify', '/check_token']:
        service_name = 'auth'
        REQUEST_DURATION.labels(
            method=request.method,
            service=service_name,
            endpoint=request.url.path
        ).observe(process_time)
        REQUEST_COUNT.labels(
            method=request.method,
            service=service_name,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

    return response

app.include_router(auth_router, tags=['auth'])
