from fastapi import FastAPI
import uvicorn

from src.routers.schedule import router as schedule_router

app = FastAPI(title="Carbon-Aware Scheduler")
app.include_router(schedule_router, prefix="/v0")


@app.get("/")
async def root():
    return {"message": "Carbon-Aware Scheduler"}


def main():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True, timeout_keep_alive=30)


if __name__ == "__main__":
    main()
