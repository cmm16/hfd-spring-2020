import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from multiprocessing import Pool
from os import path
from os import getcwd


class SpatialJoin:
    def __init__(self, path_to_geojson, point_data):
        """
        Spatial join class which is used to spatially join geojson file to point data

        Arguments:
            path_to_geojson (str): String path to geojson csv file
            point_data (df): Pandas data frame of point data (typically either inc or unit data)
        """
        print(path_to_geojson)
        self.geo_map = gpd.read_file(path_to_geojson)
        self.point_data = point_data
        # compute list of point type object row[4] is for longitude and row[5] os for latitude
        self.points = [Point(row[4], row[5]) for row in self.point_data.values]

    def id_fips_codes(self):
        """
        Function sync multiprocess self.points on method self.geo_map_point mapping the fips code for each point

        Returns
            (list): A list of 15 digit fips codes of the length of the number of input points

        """
        with Pool() as p:
            result = p.map(self.geo_map_point, self.points)
        return result

    def geo_map_point(self, point):
        """
        Maps single input point to its 15 digit fips code based on the geojson data frame

        Arguments:
            point (Point): Point type object trying to be spatially placed in the geojson file
        Returns:
            (int) If valid match found returns 15 digit fips code, (None) if no match returns None, (int) returns -1 if
            multiple matches are found since this should not occur

        """
        FIPS = self.geo_map[self.geo_map["geometry"].contains(point)]["FIPS"].values
        if len(FIPS) == 1:
            return FIPS[0]
        elif len(FIPS) > 1:
            return -1
        else:
            return None

    def spatial_join_and_save(self):
        """
        Spatially joins and saves data so that each row in the point df will have a corresponding 15 digit fips code

        Returns:
            (DataFrame): Returns a data frame that includes location
        """
        locations = self.id_fips_codes()
        self.point_data["location"] = locations
        return self.point_data
