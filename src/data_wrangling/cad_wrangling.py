import pandas as pd
import numpy as np
from os import listdir
from os import path
from os import getcwd
from zipfile import ZipFile

# look at why there are duplicates
# determine all column names
# find good way to distinguish cad unit and incident
# determine what "-" file is


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
            with ZipFile(path_to_zip, "r") as zipObj:
                # will place all unzipped files in save_directory, will write over the old files so creating
                # duplicates by running function multiple times is not possible
                zipObj.extractall(save_directory)


def merge_csvs(directory):
    """
    Merges all the csvs in a target directory with a certain naming convention return result as a single numpy array

    Arguments:
        directory (str): String path to directory with csvs to be merged

    Returns:
        (numpy array): Numpy array that is the values of all the merged csvs
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
            df_values = np.delete(
                df.values, [len(df.values) - 1, len(df.values) - 2], axis=0
            )
            # add column names to values since these are actually the first valid row
            first_valid_row = df.columns.values.reshape((1, 6))
            df_ar = np.append(df_values, np.reshape(first_valid_row, (1, 6)), axis=0)
            ar = np.append(ar, df_ar, axis=0)
    return ar


def clean_inc_unit(ar):
    """
    Cleans and formats incident unit data numpy array

    Arguments:
        ar (numpy array): Numpy array of incident unit data from merge_csvs

    Returns:
        (numpy array): Numpy array cleaned of incident unit data
    """
    merged_df = pd.DataFrame(ar)
    # split the two columns that have space as their delimiter instead of comma
    split_df1 = merged_df[4].str[1:-1].str.split(" ", expand=True)
    split_df2 = merged_df[5].str[1:-1].str.split(" ", expand=True)
    final_merged_df = pd.concat([merged_df[[0, 1, 2]], split_df1, split_df2], axis=1)
    return final_merged_df.values


def save_clean_ar(directory, ar, column_names):
    """
    Saves clean data to a target directory

    Arguments:
        directory (str): String path to the desired save location
        ar (numpy array): Numpy array of cleaned data
        column_names (list(str)): List of string names representing each columns name of the numpy array
    """
    pd.DataFrame(ar, columns=column_names).to_csv(directory)


def wrangle_cad_unit(directory):
    """
    Runs all functions needed to wrangle the cad incident unit data given a target data base directory

    Arguments:
        directory (str): String path to the data folder
    """
    zip_cad_path = path.join(directory, "UPDATE CAD DATA/")
    unzip_cad_path = path.join(directory, "unzip_cad")
    clean_cad_path = path.join(directory, "clean_cad.csv")
    unzip_folders(zip_cad_path, unzip_cad_path)
    ar = merge_csvs(unzip_cad_path)
    clean_ar = clean_inc_unit(ar)
    # add names as list instead of range
    save_clean_ar(clean_cad_path, clean_ar, list(range(7)))




def main():
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    wrangle_cad_unit(data_dir)

if __name__ == '__main__':
    main()
