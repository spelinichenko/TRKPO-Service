import pandas as pd

from src.models.enums import District

district_to_url = {
    District.admiralteysky: "150",
    District.central: "133",
    District.frunzensky: "134",
    District.kalininsky: "147",
    District.kirovsky: "146",
    District.kolpinsky: "145",
    District.krasnogvardeisky: "144",
    District.krasnoselsky: "143",
    District.kurortny: "141",
    District.moscow: "140",
    District.nevsky: "139",
    District.petrodvortsovy: "137",
    District.petrogradsky: "138",
    District.primorsky: "136",
    District.pushkinsky: "135",
    District.vasileostrovsky: "149",
    District.vyborg: "148",
}

def get_dataframe_by_district(district: District) -> pd.DataFrame:
    return pd.read_excel(
        f"https://spb.cian.ru/export/xls/offers/?deal_type=rent&district%5B0%5D={district_to_url[district]}&engine_version=2&offer_type=offices&office_type%5B0%5D=4"
    )