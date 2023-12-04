from contextlib import asynccontextmanager
from fastapi import FastAPI
import pandas as pd

from src.models.models import MainResponse
from src.models.enums import District

district_to_url = {
    District.admiralteysky: "admiralteyskiy-04150",
    District.central: "centralnyy-04133",
    District.frunzensky: "frunzenskiy-04134",
    District.kalininsky: "kalininskiy-04147",
    District.kirovsky: "kirovskiy-04146",
    District.kolpinsky: "kolpinskiy-04145",
    District.krasnogvardeisky: "krasnogvardeyskiy-04144",
    District.krasnoselsky: "krasnoselskiy-04143",
    District.kurortny: "kurortnyy-04141",
    District.moscow: "moskovskiy-04140",
    District.nevsky: "nevskiy-04139",
    District.petrodvortsovy: "petrodvorcovyy-04137",
    District.petrogradsky: "petrogradskiy-04138",
    District.primorsky: "primorskiy-04136",
    District.pushkinsky: "pushkinskiy-04135",
    District.vasileostrovsky: "vasileostrovskiy-04149",
    District.vyborg: "vyborgskiy-04148",
}

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


def get_dataframe_by_district(district: District) -> pd.DataFrame:
    return pd.read_excel(
        f"https://spb.cian.ru/snyat-pomeshenie-pod-obshepit-sankt-peterburg-{district_to_url[district]}"
    )
