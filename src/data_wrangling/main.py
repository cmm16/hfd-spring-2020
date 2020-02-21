from os import path
from os import getcwd
from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.aggregate import aggregate
from src.data_wrangling.test_train_split import test_train_split
from src.data_wrangling.merge_on_bg import merge_by_bg, aggregate_acres_fips_to_bg


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
    geojson_data_path = path.join(
        data_dir,
        "Uploaded_Shapefiles/CensusBlock_2010/censusblock_2010_clip_by_fir.geojson",
    )
    geo_join_save_path = path.join(data_dir, "inc_cad_clean_with_loc.csv")
    spatial_join(geojson_data_path, inc_save_path, geo_join_save_path)

    # performs group by on specified columns
    group_columns = ["Block_Group", "Call_Type"]
    groupby_save_path = path.join(data_dir, "bg_call_type_aggregate.csv")
    aggregate(geo_join_save_path, group_columns, groupby_save_path)

    acres_path = path.join(data_dir, "acres.csv")
    aggregate_acres_fips_to_bg(geojson_data_path, acres_path)

    path_to_census = path.join(
        data_dir,
        "Census Data/census_hfd_counties_BG.csv"
    )
    census_save_path = path.join(data_dir, "census_merged.csv")
    merge_by_bg(
        groupby_save_path, path_to_census, "Block_Group", "GeoID17bg", census_save_path
    )
    merge_by_bg(
        census_save_path, acres_path, "Block_Group", "Block_Group", census_save_path
    )

    train_save_path = path.join(data_dir, "bg_inc_train.csv")
    test_save_path = path.join(data_dir, "bg_inc_test.csv")
    test_train_split(census_save_path, train_save_path, test_save_path)


if __name__ == "__main__":
    main()
