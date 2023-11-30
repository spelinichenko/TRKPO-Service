from fastapi import APIRouter

from src.models.models import MainRequest, MainResponse
from src.utils.utils import mock_response

router = APIRouter(prefix="/trkpo")


@router.post("/request")
async def get_best_places(main_request: MainRequest) -> MainResponse:
    return mock_response
