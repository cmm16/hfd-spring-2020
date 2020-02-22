from os import path
from os import getcwd
from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import SpatialJoin
from src.data_wrangling.aggregate import aggregate
from src.data_wrangling.test_train_split import test_train_split
from src.data_wrangling.merge_on_bg import merge_by_bg, aggregate_acres_fips_to_bg


def main():
    # set data directory to base plus /data
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    # unzip merge and clean csvs saving to save path location

    inc_df = cad_wrangling(data_dir, inc_type="inc", unzip=True)
    unit_df = cad_wrangling(data_dir, inc_type="unit", unzip=True)

    # performs spatial join on geojson data and points data saving to save path location
    geojson_data_path = path.join(
        data_dir,
        "Uploaded_Shapefiles/CensusBlock_2010/censusblock_2010_clip_by_fir.geojson",
    )
    geo_join_save_path = path.join(data_dir, "inc_cad_clean_with_loc.csv")
    spatial_join = SpatialJoin(geojson_data_path, inc_df)
    spatial_join_df = spatial_join.spatial_join_and_save()

    # performs group by on specified columns
    group_columns = ["Block_Group", "Call_Type"]
    aggregate_df = aggregate(spatial_join_df, group_columns)

    # calculate arces
    acres_path = path.join(data_dir, "acres.csv")
    aggregate_acres_fips_to_bg(geojson_data_path, acres_path)

    # merge census data, acres data, and call grouped by bg data
    path_to_census = path.join(data_dir, "Census Data/census_hfd_counties_BG.csv")
    census_save_path = path.join(data_dir, "census_merged.csv")
    merge_by_bg(
        groupby_save_path, path_to_census, "Block_Group", "GeoID17bg", census_save_path
    )
    merge_by_bg(
        census_save_path, acres_path, "Block_Group", "Block_Group", census_save_path
    )

    # perform test train split and save
    train_save_path = path.join(data_dir, "train_wrangled.csv")
    test_save_path = path.join(data_dir, "test_wrangled.csv")
    test_train_split(census_save_path, train_save_path, test_save_path)


if __name__ == "__main__":
    main()
