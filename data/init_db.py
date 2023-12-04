import osmnx as ox
import geopandas as gpd
import pandas as pd
import geopandas as gpd
from pymongo import MongoClient
from os import environ as env

def get_spb_boundaries():
    spb = ox.geocode_to_gdf("R337422", by_osmid=True)
    return spb.geometry.iloc[0]

def get_spb_districts_from_osm(spb_boundaries) -> gpd.GeoDataFrame:
    districts = [
        "Приморский район", 
        "Московский район",
        "Курортный район",
        "Центральный район",
        "Пушкинский район",
        "Фрунзенский район",
        "Василеостровский район",
        "Колпинский район",
        "Петроградский район",
        "Кронштадтский район",
        "Красносельский район",
        "Кировский район",
        "Петродворцовый район",
        "Адмиралтейский район",
        "Невский район",
        "Калининский район",
        "Красногвардейский район",
        "Выборгский район"
    ]
    spb_districts = ox.features_from_polygon(spb_boundaries, tags={"name":districts})
    spb_districts = spb_districts.dropna(subset=['addr:region'])
    spb_districts = spb_districts[spb_districts['addr:region'] != 'Ленинградская область']
    spb_districts = spb_districts.reset_index()[['geometry', "name"]]
    return spb_districts

def get_spb_food_places_from_osm(spb_boundaries) -> gpd.GeoDataFrame:
    tags = {
        "amenity": ["bar", 	"biergarten", "cafe", "fast_food", "food_court", "ice_cream", "pub", "restaurant"]
    }
    needed_columns = ["geometry", "opening_hours", "cuisine", "amenity", "food", "delivery", "name"]
    data = ox.features_from_polygon(spb_boundaries, tags=tags).reset_index()[needed_columns]
    return data

def spatial_join_food_places_and_districts(food_places: gpd.GeoDataFrame, districts: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.sjoin(food_places, districts).rename(columns={'name_left': 'name', 'name_right': 'district'}).drop(columns=['index_right'])

def preprocess_raw_data(food_places_and_districts: gpd.GeoDataFrame):
    pass

def insert_to_db():
    mongodb_uri = env.get("MONGODB_URI")
    mongo_client = MongoClient(mongodb_uri)
    try:
        mongo_client.server_info()
    except Exception as e:
        print(f"Cannot establish connection to MongoDB: {e}")
        return
    
    collection = mongo_client.get_database('trkpo').get_collection('osm_food_places')
    collection.insert_one({"aboba": "boba"})
