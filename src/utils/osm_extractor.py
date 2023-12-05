import osmnx as ox
import geopandas as gpd
import geopandas as gpd
from src.models.enums import District
import random

def get_spb_boundaries():
    spb = ox.geocode_to_gdf("R337422", by_osmid=True)
    return spb.geometry.iloc[0]


def get_spb_district_from_osm(spb_boundaries, district: District) -> gpd.GeoDataFrame:
    districts_to_names = {
        District.primorsky:"Приморский район", 
        District.moscow:"Московский район",
        District.kurortny:"Курортный район",
        District.central:"Центральный район",
        District.pushkinsky:"Пушкинский район",
        District.frunzensky:"Фрунзенский район",
        District.vasileostrovsky:"Василеостровский район",
        District.kolpinsky:"Колпинский район",
        District.petrogradsky:"Петроградский район",
        District.krasnoselsky:"Красносельский район",
        District.kirovsky:"Кировский район",
        District.petrodvortsovy:"Петродворцовый район",
        District.admiralteysky: "Адмиралтейский район",
        District.nevsky:"Невский район",
        District.kalininsky:"Калининский район",
        District.krasnogvardeisky:"Красногвардейский район",
        District.vyborg:"Выборгский район"
    }
    spb_district = ox.features_from_polygon(spb_boundaries, tags={"name": districts_to_names[district]})
    spb_district = spb_district.dropna(subset=['addr:region'])
    spb_district = spb_district[spb_district['addr:region'] != 'Ленинградская область']
    spb_district = spb_district.reset_index()[['geometry', "name"]]
    return spb_district

def get_spb_food_places_by_district(spb_district) -> gpd.GeoDataFrame:
    tags = {
        "amenity": ["cafe", "fast_food", "food_court", "restaurant"]
    }
    data = ox.features_from_polygon(spb_district.geometry.iloc[0], tags=tags).reset_index()
    return data

def spatial_join_food_places_and_district(food_places: gpd.GeoDataFrame, district_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.sjoin(food_places, district_gdf).rename(columns={'name_left': 'name', 'name_right': 'district'}).drop(columns=['index_right'])

def preprocess_raw_data(food_places_and_districts):
    needed_columns = ["geometry", "opening_hours", "cuisine", "amenity", "delivery", "name", "district"]
    food_places_and_districts: gpd.GeoDataFrame = food_places_and_districts.loc[:, needed_columns]
    food_places_and_districts: gpd.GeoDataFrame = food_places_and_districts[food_places_and_districts['cuisine'] != 'coffee_shop']
    map = {
        "delivery": {
            "yes" : True,
            "only": True,
            "no": False,
            "limited": True,
            "Mo-Su 08:00-22:00": True,
            "12:00-23:00": True,
            "11:00-21:00": True,
            "Mo-Su 11:00-22:00": True,
            "10:00-23:00": True,
            "10:00-21:00": True,
            "10:00-20:00": True,
            "12:30-21:00": True,
            "12:00-21:00": True,
            "11:30-17:00": True
        },
        "amenity": {
            "fast_food": "canteen",
            "food_court": "canteen"
        }
    }
    food_places_and_districts.replace(map, inplace=True)
    food_places_and_districts['delivery'] = food_places_and_districts.apply((lambda x: random.choice([True, False])), axis=1)

    time_pattern = r'(\d{2}:\d{2}-\d{2}:\d{2})'
    food_places_and_districts['opening_hours'] = food_places_and_districts['opening_hours'].str.extract(time_pattern)
    food_places_and_districts['opening_hours'].bfill(inplace=True)
    food_places_and_districts['opening_hours'].ffill(inplace=True)
    open_close_time_pattern = r'(\d{2}):(\d{2})-(\d{2}):(\d{2})'
    food_places_and_districts['open_time'] = food_places_and_districts['opening_hours'].str.extract(open_close_time_pattern)[0].astype(int)
    food_places_and_districts['close_time'] = food_places_and_districts['opening_hours'].str.extract(open_close_time_pattern)[2].astype(int)
    cuisine_map = {
        'kebab': 'uzbekistan',
        'burger': 'mexico',
        'georgian': 'georgia',
        'pizza': 'italy',
        'shawarma': 'uzbekistan',
        'sushi': 'japan',
        'chinese': 'china',
        'italian': 'italy',
        'russian': 'russia',
        'japanese': 'japan',
        'korean': 'korea',
        'mexican': 'mexico',
        'local': 'russia',
        'doner': 'uzbekistan',
        'ramen': 'japan',
        'ukrainian': 'russia'
    }
    food_places_and_districts['cuisine'] = food_places_and_districts['cuisine'].map(cuisine_map)
    food_places_and_districts['cuisine'].bfill(inplace=True)
    food_places_and_districts['cuisine'].ffill(inplace=True)
    return food_places_and_districts

def get_preprocessed_data_by_district(district: District) -> gpd.GeoDataFrame:
    spb_boundaries = get_spb_boundaries()
    district_info = get_spb_district_from_osm(spb_boundaries, district)
    food_places = get_spb_food_places_by_district(district_info)
    food_places_with_district = spatial_join_food_places_and_district(food_places, district_info)
    preprocessed_food_places_with_district = preprocess_raw_data(food_places_with_district)
    return preprocessed_food_places_with_district
