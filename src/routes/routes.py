from fastapi import APIRouter

from src.processing.processing import get_places
from src.models.models import MainRequest, MainResponse

router = APIRouter(prefix="/trkpo")


@router.post("/request")
async def get_best_places(main_request: MainRequest) -> list[MainResponse]:
    return get_places(main_request)
