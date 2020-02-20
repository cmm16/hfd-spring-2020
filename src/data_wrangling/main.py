from os import path
from os import getcwd
from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.aggregate import aggregate


def main():
    # set data directory to base plus /data
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    # unzip merge and clean csvs saving to save path location
    # for incidents csvs
    inc_save_path = path.join(data_dir, "inc_cad_clean.csv")
    cad_wrangling(data_dir, inc_save_path, inc_type="inc", unzip=True)
    # for unit csvs
    unit_save_path = path.join(data_dir, "unit_cad_clean.csv")
    cad_wrangling(data_dir, unit_save_path, inc_type="unit", unzip=True)

    # performs spatial join on geojson data and points data saving to save path location
    geojson_data_path = path.join(data_dir, "Uploaded_Shapefiles/CensusBlock_2010/censusblock_2010_clip_by_fir.geojson")
    points_data_path = path.join(data_dir, "inc_cad_clean.csv")
    geo_join_save_path = path.join(data_dir, "inc_cad_clean_with_loc.csv")
    spatial_join(geojson_data_path, points_data_path, geo_join_save_path)

    # performs group by on specified columns
    path_to_groupby_data = path.join(data_dir, "inc_cad_clean_with_loc.csv")
    group_columns = ["Block_Group", "Call_Type"]
    groupby_save_path = path.join(data_dir, "bg_call_type_aggregate.csv")
    aggregate(path_to_groupby_data, group_columns, groupby_save_path)


if __name__ == "__main__":
    main()
