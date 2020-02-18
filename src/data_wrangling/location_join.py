import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from multiprocessing import Pool


class SpatialJoin:
    def __init__(self, path_to_geojson, path_to_point_data):
        self.geo_map = gpd.read_file(path_to_geojson)
        self.point_data = pd.read_csv(path_to_point_data)
        self.points = [Point(row["Longitude"], row["Latitude"]) for row in self.point_data]

    def id_fips_codes(self):
        with Pool() as p:
            result = p.map(self.geo_map_point, self.points)
        return result

    def geo_map_point(self, point):
        FIPS = self.geo_map[self.geo_map["geometry"].contains(point)]["FIPS"].values
        if len(FIPS) == 1:
            return FIPS[0]
        elif len(FIPS) > 1:
            return -1
        else:
            return None

    def spatial_join_and_save(self, save_name):
        locations = self.id_fips_codes()
        self.point_data["location"] = locations
        self.point_data.to_csv(save_name, index=False)


