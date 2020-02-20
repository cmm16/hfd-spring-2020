import pandas as pd


def merge_by_bg(path_to_new_data, path_to_bg_data, merge_column_name, save_path):
    new_df = pd.read_csv(path_to_new_data)
    bg_df = pd.read_csv(path_to_bg_data)
    bg_df.merge(new_df, left_on="Block_Group", right_on=merge_column_name).to_csv(save_path)

