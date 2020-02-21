import pandas as pd


def merge_by_bg(path_to_data1, path_to_data2, merge_column_name1, merge_column_name2, save_path):
    """
    Merges two data frames with common bg key column

    path_to_data1 (str): String path data to be merged
    path_to_data2 (str): String path to block group data
    merge_column_name (str): String name of column to merge on in merge data
    save_path (str): String path to desired save location
    """
    df1 = pd.read_csv(path_to_data1)
    df2 = pd.read_csv(path_to_data2)
    merged_df = df1.merge(df2, left_on=merge_column_name1, right_on=merge_column_name2)
    merged_df.to_csv(save_path, index=False)

