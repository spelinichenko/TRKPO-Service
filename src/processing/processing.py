import geopandas as gpd
from geopy.geocoders import Photon
from shapely.geometry import Point

from src.models.models import CafeType, MainRequest, MainResponse
from src.utils.osm_extractor import get_preprocessed_data_by_district
from src.utils.utils import get_dataframe_by_district


def get_places(request: MainRequest) -> list[MainResponse]:
    osm_data = get_preprocessed_data_by_district(request.district)
    cian_data = get_dataframe_by_district(request.district)
    cian_data["Цена"] = cian_data["Цена"].str.extract(r"(\d+)", expand=False).astype(int)
    cian_data["Площадь"] = cian_data["Площадь"].str.extract(r"(\d+)", expand=False).astype(float)
    # filter cian_objects by cost
    cian_data = cian_data[cian_data["Цена"] <= request.budget]
    map_cafe_type_to_kitchen_area = {CafeType.cafe: 10, CafeType.restaurant: 15, CafeType.canteen: 5}
    cian_data = cian_data[
        cian_data["Площадь"] >= request.visitor_capacity * 2 + map_cafe_type_to_kitchen_area[request.cafe_type]
    ]
    geolocator = Photon()
    cian_data["geometry"] = cian_data.apply(lambda x: geolocator.geocode(x["Адрес"]), axis=1)
    cian_data["geometry"] = cian_data.apply(lambda x: Point(x.geometry.longitude, x.geometry.latitude), axis=1)
    cian_data_gdf = gpd.GeoDataFrame(cian_data, geometry=cian_data["geometry"], crs="EPSG:4326")
    cian_data_gdf = cian_data_gdf.to_crs(cian_data_gdf.estimate_utm_crs())
    cian_data_gdf["buffer"] = cian_data_gdf["geometry"].buffer(1000).to_crs("EPSG:4326")
    cian_data_gdf["geometry"] = cian_data_gdf["geometry"].to_crs("EPSG:4326")
    cian_data_gdf = cian_data_gdf.set_geometry(cian_data_gdf["buffer"])
    cian_osm_data_gdf = gpd.sjoin(osm_data, cian_data_gdf, lsuffix="cian", rsuffix="osm")
    osm_food_places_amount = (
        cian_osm_data_gdf.groupby("ID  объявления")["ID  объявления"].count().reset_index(name="places_count")
    )
    cian_osm_data_gdf = cian_osm_data_gdf.merge(osm_food_places_amount, on="ID  объявления")

    delivery_percent = (
        cian_osm_data_gdf.groupby("ID  объявления")["delivery"]
        .value_counts(normalize=True)
        .reset_index(name="delivery_percent")
    )
    delivery_percent["suggest_delivery"] = delivery_percent.apply(
        lambda x: x["delivery"] is True and x["delivery_percent"] < 0.5, axis=1
    )
    delivery_suggestion = (
        delivery_percent.groupby("ID  объявления")["suggest_delivery"]
        .sum()
        .astype(bool)
        .reset_index(name="suggest_delivery")
    )

    best_place = cian_osm_data_gdf.merge(delivery_suggestion, on="ID  объявления")
    suggest_open_time = best_place.groupby("ID  объявления")["open_time"].min().reset_index(name="suggest_open_time")
    suggest_close_time = best_place.groupby("ID  объявления")["close_time"].max().reset_index(name="suggest_close_time")
    best_place = best_place.merge(suggest_open_time, on="ID  объявления")
    best_place = best_place.merge(suggest_close_time, on="ID  объявления")
    best_place["Улица"] = best_place["Адрес"].str.split(pat=",").str[1].str.strip()
    short_best_place = (
        best_place[
            [
                "Улица",
                "Адрес",
                "Площадь",
                "Цена",
                "suggest_open_time",
                "suggest_close_time",
                "suggest_delivery",
                "ID  объявления",
                "places_count",
                "Ссылка на объявление",
            ]
        ]
        .drop_duplicates()
        .sort_values("places_count")
        .head(5)
        .to_dict("records")
    )
    list_of_responces = [
        MainResponse(
            street=x["Улица"],
            accuracy_address=x["Адрес"],
            room_area=x["Площадь"],
            room_price=x["Цена"],
            working_hours=f'{x["suggest_open_time"]}:00-{x["suggest_close_time"]}:00',
            delivery=x["suggest_delivery"],
            link=x["Ссылка на объявление"],
        )
        for x in short_best_place
    ]
    return list_of_responces
