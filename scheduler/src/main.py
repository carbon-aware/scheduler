import logging

import uvicorn
from fastapi import FastAPI
from pythonjsonlogger.json import JsonFormatter

from src.routers.regions import router as regions_router
from src.routers.schedule import router as schedule_router
from src.utils.logging import add_request_logging

logging.basicConfig(level=logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger()
logger.addHandler(handler)

app = FastAPI(title="Carbon-Aware Scheduler")
app.include_router(schedule_router, prefix="/v0")
app.include_router(regions_router, prefix="/v0")

add_request_logging(app)


@app.get("/")  # type: ignore[misc]
async def root() -> dict[str, str]:
    return {"message": "Carbon-Aware Scheduler"}


@app.get("/health")  # type: ignore[misc]
async def health() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True, timeout_keep_alive=30)


if __name__ == "__main__":
    main()
