from multiprocessing import Pool

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


class SpatialJoin:
    def __init__(self, path_to_geojson, path_to_point_data):
        """
        Spatial join class which is used to spatially join geojson file to point data

        Arguments:
            path_to_geojson (str): String path to geojson csv file
            path_to_point_data (str): String path to point data csv file
        """
        self.geo_map = gpd.read_file(path_to_geojson)
        self.point_data = pd.read_csv(path_to_point_data)
        # compute list of point type object row[4] is for longitude and row[5] os for latitude
        self.points = [Point(row[5], row[6]) for row in self.point_data.values]

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
        FIPS = self.geo_map[self.geo_map["geometry"].contains(point)]["Name"].values
        if len(FIPS) == 1:
            return FIPS[0]
        elif len(FIPS) > 1:
            return -1
        else:
            return None

    def spatial_join_and_save(self, save_name):
        """
        Spatially joins and saves data so that each row in the point df will have a corresponding 15 digit fips code

        Arguments:
            save_name (str): String path name for the desired save location for the output data csv
        """
        locations = self.id_fips_codes()
        self.point_data["location"] = locations
        self.point_data.to_csv(save_name, index=False)


def spatial_join(path_to_geojson, path_to_point_data, save_path):
    """
    Instantiates SpatialJoin class and then performs join saving the result

    Arguments:
        path_to_geojson (str): String path to geojson data
        path_to_point_data (str): String path to point data
        save_path (str): String path to where save results should go
    """
    sp = SpatialJoin(path_to_geojson, path_to_point_data)
    sp.spatial_join_and_save(save_path)
