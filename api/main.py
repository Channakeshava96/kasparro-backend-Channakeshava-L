from fastapi import FastAPI, Request
import time
import uuid

from api.data import router as data_router
from api.health import router as health_router

app = FastAPI(title="Kasparro Backend API")


@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    latency_ms = int((time.time() - start_time) * 1000)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-API-Latency-ms"] = str(latency_ms)

    return response


app.include_router(data_router)
app.include_router(health_router)
