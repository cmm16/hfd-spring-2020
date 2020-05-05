from os.path import join, dirname
from os import getcwd
from src.data_wrangling.imagetrend_wrangling import wrangle_image_trend, dropAirports
from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.aggregate import aggregate, image_trend_aggregate
from src.data_wrangling.test_train_split import test_train_split
from src.data_wrangling.merge_on_bg import merge_by_bg, aggregate_acres_fips_to_bg
from src.data_wrangling.model_prep import model_prep
import pandas as pd

def main(data_dir):
    # set data directory to base plus /data
    image_trend_data_path = join(data_dir, "Final Datasets")
    image_trend_wrangled_path = join(data_dir, "imagetrend.csv")
    #wrangle_image_trend(image_trend_data_path, image_trend_wrangled_path)

    # performs spatial join on geojson data and points data saving to save path location
    geojson_data_path = join(
        data_dir,
        "Uploaded_Shapefiles/CensusBlock_2010/Census_FIP12_within_Fire_Dis.geojson",
    )
    geo_join_save_path = join(data_dir, "inc_cad_clean_with_loc.csv")
    #spatial_join(geojson_data_path, image_trend_wrangled_path, geo_join_save_path)

    # performs group by on specified columns
    group_columns = ["Block_Group", "Event_Type"]
    groupby_save_path = join(data_dir, "bg_call_type_aggregate.csv")
    df = image_trend_aggregate(pd.read_csv(geo_join_save_path))

    #drop air ports
    df = dropAirports(df)
    post_airports = join(data_dir, "post_airports.csv")
    df.to_csv(join(data_dir, post_airports))

    # calculate arces
    #acres_path = path.join(data_dir, "acres.csv")
    #acres_data_path = path.join(
    #    data_dir,
    #    "Uploaded_Shapefiles/CensusBlock_2010/Census_2010_Clip_by_Har.geojson",
    #)
    #aggregate_acres_fips_to_bg(acres_data_path, acres_path)

    # merge census data, acres data, and call grouped by bg data
    path_to_census = join(data_dir, "Census Data/census_hfd_counties_BG.csv")
    census_save_path = join(data_dir, "census_merged.csv")
    merge_by_bg(
        post_airports, path_to_census, "Block_Group", "GeoID17bg", census_save_path
    )

    x_df, _, y_df = model_prep(pd.read_csv(census_save_path))

    print(x_df, y_df)


    #merge_by_bg(
    #    census_save_path, acres_path, "Block_Group", "Block_Group", census_save_path
    #)

    # perform test train split and save
    x_train_save_path = join(data_dir, "x_train.csv")
    y_train_save_path = join(data_dir, "y_train.csv")
    x_test_save_path = join(data_dir, "x_test.csv")
    y_test_save_path = join(data_dir, "y_test.csv")
    train_x, test_x, train_y, test_y = test_train_split(x_df, y_df)

    train_x.to_csv(x_test_save_path)
    train_y.to_csv(y_test_save_path)
    test_x.to_csv(x_test_save_path)
    test_y.to_csv(y_test_save_path)

if __name__ == "__main__":
    main(join(dirname((dirname(getcwd()))), "Data"))

