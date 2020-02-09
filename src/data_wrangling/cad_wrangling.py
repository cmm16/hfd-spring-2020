import pandas as pd
import numpy as np
from os import listdir
from os import path
from zipfile import ZipFile


def unzip_folders(target_directory, save_directory):
    """
    unzips all the zip folders in a specified directory and stores all the unzipped files in a new directory

    Arguments:
        target_directory (str): String path to the directory with zip files
        save_directory (str): String path to the directory to place unzipped files
    """
    for file in listdir(target_directory):
        # currently does not have proper error handling
        if file.endswith("zip"):
            path_to_zip = path.join(target_directory, file)
            with ZipFile(path_to_zip, 'r') as zipObj:
                # will place all unzipped files in save_directory, will write over the old files so creating
                # duplicates by running function multiple times is not possible
                zipObj.extractall(save_directory)


def merge_csvs(directory):
    """
    Merges all the csvs in a target directory with a certain naming convention return result as a single numpy array

    Arguments:
        directory (str): String path to directory with csvs to be merged

    Returns:
        ar (numpy array): Numpy array that is the values of all the merged csvs
    """
    # place holder array
    ar = np.ndarray((0, 6))
    for file in listdir(directory):
        # logic statement to differentiate incident and incident unit
        if file.startswith("inc_unit"):
            path_to_csv = path.join(directory, file)
            # skip first line since this is sql garbage, will make first actual row into column names
            df = pd.read_csv(path_to_csv, skiprows=1)
            # take df values and remove two last lines that are sql garbage
            df_values = np.delete(df.values, [len(df.values)-1, len(df.values)-2], axis=0)
            # add column names to values since these are actually the first valid row
            first_valid_row = df.columns.values.reshape((1, 6))
            df_ar = np.append(df_values, np.reshape(first_valid_row, (1, 6)), axis=0)
            ar = np.append(ar, df_ar, axis=0)
    return ar


def clean_inc_unit(ar):
    merged_df = pd.DataFrame(ar)
    # split the two columns that have space as their delimiter instead of comma
    split_df1 = merged_df[4].str[1:-1].str.split(" ", expand=True)
    split_df2 = merged_df[5].str[1:-1].str.split(" ", expand=True)
    final_merged_df = pd.concat([merged_df[[0, 1, 2]], split_df1, split_df2], axis=1)
    return final_merged_df.values


def save_clean_ar(directory, ar, column_names):
    pd.DataFrame(ar, columns=column_names).to_csv(directory)


