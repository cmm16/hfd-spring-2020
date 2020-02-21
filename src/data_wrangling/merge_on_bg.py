import pandas as pd


def merge_by_bg(path_to_merge_data, path_to_bg_data, merge_column_name, save_path):
    """
    Merges two data frames with common bg key column

    path_to_merge_data (str): String path data to be merged
    path_to_bg_data (str): String path to block group data
    merge_column_name (str): String name of column to merge on in merge data
    save_path (str): String path to desired save location
    """
    new_df = pd.read_csv(path_to_merge_data)
    bg_df = pd.read_csv(path_to_bg_data)
    merged_df = bg_df.merge(new_df, left_on="Block_Group", right_on=merge_column_name).to_csv(save_path)
    merged_df.to_csv(save_path)

