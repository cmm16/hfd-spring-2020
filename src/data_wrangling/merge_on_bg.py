import geopandas as gpd
import pandas as pd


def merge_by_bg(
    path_to_data1, path_to_data2, merge_column_name1, merge_column_name2, save_path
):
    """
    Merges two data frames with common bg key column

    Inputs: 
    path_to_data1 (str): String path data to be merged
    path_to_data2 (str): String path to block group data
    merge_column_name (str): String name of column to merge on in merge data
    save_path (str): String path to desired save location
    """
    df1 = pd.read_csv(path_to_data1)
    df2 = pd.read_csv(path_to_data2)
    merged_df = df1.merge(
        df2, how="left", left_on=merge_column_name1, right_on=merge_column_name2
    )
    merged_df.to_csv(save_path, index=False)


def aggregate_acres_fips_to_bg(path_to_data, save_path):
    """
    Aggregates shape file with fips code to the block group level computing the acres of each bg

    Arguments:
            path_to_data (str): String path to data
            save_path (str): String path to desired save location
    """
    shape_df = gpd.read_file(path_to_data)
    shape_df = shape_df.rename({"Name": "FIPS"}, axis=1)
    shape_df["Block_Group"] = shape_df["FIPS"].astype(str).str[:12]
    grouped_df = shape_df.groupby(["Block_Group"]).sum()
    acres_df = pd.DataFrame(
        zip(grouped_df.index, grouped_df.Acres), columns=["Block_Group", "Acres"]
    )
    acres_df.to_csv(save_path, index=False)
