from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.models.models import MainResponse

mock_response = MainResponse(
    street="test",
    coordinates=[0.1, 0.1],
    accuracy_address="test",
    room_area=123,
    room_price=123,
    working_hours="test",
    delivery=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # PUT BD SCRIPT HERE
    yield
