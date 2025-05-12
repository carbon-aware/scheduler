import uvicorn
from fastapi import FastAPI

from src.routers.schedule import router as schedule_router

app = FastAPI(title="Carbon-Aware Scheduler")
app.include_router(schedule_router, prefix="/v0")


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
