from os import getcwd
from os.path import join, dirname

import pandas as pd

from src.data_wrangling.aggregate import image_trend_aggregate
from src.data_wrangling.covid_risk_incides import (
    CovidRiskCalculator,
    aggregate_covid_to_fire_dist,
)
from src.data_wrangling.imagetrend_wrangling import dropAirports
from src.data_wrangling.merge_on_bg import merge_by_bg
from src.data_wrangling.model_prep import model_prep
from src.data_wrangling.test_train_split import test_train_split
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.imagetrend_wrangling import wrangle_image_trend


def main(data_dir, args):
    """
    Main function that handles entire wrangling (general and covid). 
    """
    # set data directory to base plus /data
    image_trend_data_path = join(data_dir, "Final Datasets")
    image_trend_wrangled_path = join(data_dir, "imagetrend.csv")
    wrangle_image_trend(image_trend_data_path, image_trend_wrangled_path, args)

    # performs spatial join on geojson data and points data saving to save path location
    geojson_data_path = join(
        data_dir,
        join("Uploaded_Shapefiles", join("CensusBlock_2010", "Census_FIP12_within_Fire_Dis.geojson")))


    geo_join_save_path = join(data_dir, "inc_cad_clean_with_loc.csv")
    if args["small"] is not None:
        geo_join_save_path = join(data_dir, "small_inc_cad_clean_with_loc.csv")

    if args['skip'] is None:
        spatial_join(geojson_data_path, image_trend_wrangled_path, geo_join_save_path)

    # performs group by on specified columns
    groupby_save_path = join(data_dir, "bg_call_type_aggregate.csv")
    df = image_trend_aggregate(pd.read_csv(geo_join_save_path))
    df.to_csv(groupby_save_path, index=False)

    path_to_census = join(data_dir, join("Census Data","census_hfd_counties_BG.csv"))
    merge_by_bg(
        groupby_save_path,
        path_to_census,
        "Block_Group",
        "GeoID17bg",
        join(data_dir, "with_airports_for_eda.csv"),
    )

    df = dropAirports(df)
    post_airports = join(data_dir, "post_airports.csv")
    df.to_csv(join(data_dir, post_airports))

    # merge census data, and call grouped by bg data

    census_save_path = join(data_dir, "census_merged.csv")
    merge_by_bg(
        post_airports, path_to_census, "Block_Group", "GeoID17bg", census_save_path
    )

    # model prep
    x_df, _, y_df = model_prep(data_dir, pd.read_csv(census_save_path))
    # perform test train split and save
    y_df = y_df[
        [
            "Percent Fire Related Calls",
            "Percent Health Related Calls",
            "Percent Injuries External Related Calls",
            "Percent Mental Illness Related Calls",
        ]
    ]
    x_train_save_path = join(data_dir, "x_train.csv")
    y_train_save_path = join(data_dir, "y_train.csv")
    x_test_save_path = join(data_dir, "x_test.csv")
    y_test_save_path = join(data_dir, "y_test.csv")
    train_x, test_x, train_y, test_y = test_train_split(x_df, y_df)
    train_x.to_csv(x_train_save_path)
    train_y.to_csv(y_train_save_path)
    test_x.to_csv(x_test_save_path)
    test_y.to_csv(y_test_save_path)

    pd.read_csv(census_save_path).set_index("Block_Group").loc[train_x.index, :].to_csv(
        join(data_dir, "final_train_categories.csv")
    )

    # create covid data set
    covid_save_path = join(data_dir, "covid_indices.csv")
    covid_risk_calculator = CovidRiskCalculator(
        pd.read_csv(census_save_path),
        df.set_index("Block_Group"),
        data_dir,
        covid_save_path,
    )

    covid_risk_calculator.create_covid_df()

    fire_dist_save_path = join(data_dir, "firedist_covid.csv")
    block_group_covid = pd.read_csv(join(data_dir, "covid_indices.csv"))

    aggregate_covid_to_fire_dist(
        pd.read_csv(join(data_dir, "Image_Trend_Merged_SpatialJOIN.csv")),
        block_group_covid,
        fire_dist_save_path,
    )

if __name__ == "__main__":
    main(join(dirname((dirname(getcwd()))), "Data"))
