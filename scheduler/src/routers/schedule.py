import logging

from fastapi import APIRouter

from src.modeling.schedule import compute_schedule
from src.types.schedule import ScheduleRequest, ScheduleResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")  # type: ignore[misc]
async def schedule(request: ScheduleRequest) -> ScheduleResponse:
    return await compute_schedule(request)
