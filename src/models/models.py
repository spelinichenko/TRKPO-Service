from pydantic import BaseModel

from src.models.enums import District, Cuisine, CafeType


class MainRequest(BaseModel):
    district: District
    cuisine: Cuisine
    budget: int
    cafe_type: CafeType
    visitor_capacity: int


class MainResponse(BaseModel):
    street: str
    coordinates: list[float]
    accuracy_address: str
    room_area: int
    room_price: int
    working_hours: str
    delivery: bool
