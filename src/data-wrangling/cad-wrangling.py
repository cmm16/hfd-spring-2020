import pandas as pd
import numpy as np
from os import listdir
from os import path
from zipfile import ZipFile


DATA = "/Users/work/PycharmProjects/hfd-spring-2020/data/"
zip_cad_path = path.join(DATA, "UPDATE CAD DATA/")
path.join(DATA, "unzip_cad")


def unzip_folders(target_directory, save_directory):
    """
    unzips all the zip folders in a specified directory and stores all the unzipped files in a new directory

    Arguments:
        target_directory (str): String path to the directory with zip files
        save_directory (str): String path to the directory to place unzipped files
    """
    for file in listdir(target_directory):
        if file.endswith("zip"):
            path_to_zip = path.join(zip_cad_path, file)
            with ZipFile(path_to_zip, 'r') as zipObj:
                # will place all unzipped files in save_directory
                zipObj.extractall(save_directory)


def merge_csvs(directory):
    """

    Arguments:
        directory (str): String path

    Returns:

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
            df_ar = np.append(df_values, np.reshape(df.columns, (1,6)), axis=0)
            ar = np.append(ar, df_ar, axis=0)
    return ar

def clean_inc_unit(ar):


