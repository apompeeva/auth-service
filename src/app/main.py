import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from jaeger_client import Config
from opentracing import Format, global_tracer, tags
from prometheus_client import make_asgi_app

from app.config import JAEGER_AGENT_HOST, JAEGER_AGENT_PORT
from app.endpoints.endpoints import auth_router
from app.metrics import REQUEST_COUNT, REQUEST_DURATION
from app.producer.producer import producer

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание продюсера перед запуском приложения и остановка после."""
    logging.info(f'Jaeger creds: {JAEGER_AGENT_HOST}:{JAEGER_AGENT_PORT}')
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': JAEGER_AGENT_HOST,
                'reporting_port': JAEGER_AGENT_PORT,
            },
            'logging': True,
        },
        service_name='auth-service-pompeeva',
        validate=True,
    )
    tracer = config.initialize_tracer()
    try:
        await producer.start()
        yield {'jaeger_tracer': tracer}
    except:
        yield {'jaeger_tracer': tracer}
    finally:
        await producer.stop()

app = FastAPI(lifespan=lifespan)

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)


@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    """Middleware для сбора метрик."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if request.url.path in ['/auth', '/register', '/api/verify', '/check_token']:
        service_name = 'auth'
        REQUEST_DURATION.labels(
            method=request.method,
            service=service_name,
            endpoint=request.url.path,
        ).observe(process_time)
        REQUEST_COUNT.labels(
            method=request.method,
            service=service_name,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

    return response


@app.middleware('http')
async def tracing_middleware(request: Request, call_next):
    """Middleware для трассировки запросов."""
    span_ctx = global_tracer().extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f'auth_{request.method}_{request.url.path}',
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response


app.include_router(auth_router, tags=['auth'])
