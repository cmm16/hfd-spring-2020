import pandas as pd
import numpy as np
from os import listdir
from os import path
from zipfile import ZipFile


DATA = "/Users/work/PycharmProjects/hfd-spring-2020/data/"
zip_cad_path = path.join(DATA, "UPDATE CAD DATA/")


def unzip_folders(directory):
    """
    unzips all the zip folders in a specified directory and stores all the unziped files in a new directory

    Arguments:
        directory (str): a string path to the desired directory
    """
    for file in listdir(directory):
        if file.endswith("zip"):
            path_to_zip = path.join(zip_cad_path, file)
            with ZipFile(path_to_zip, 'r') as zipObj:
                zipObj.extractall(path.join(DATA, "unzip_cad"))


def merge_csvs(directory):
    """

    Arguments:

    Returns:

    """
    ar = np.ndarray((0, 6))
    for file in listdir(directory):
        if file.startswith("inc_unit"):
            path_to_csv = path.join(directory, file)
            print(file, df.columns)
            df = pd.read_csv(path_to_csv, skiprows = 1)
            df_len = len(df.values)
            df_ar = np.append(np.delete(df.values, [len(df.values) - 1, len(df.values) -2], axis = 0), np.reshape(df.columns, (1,6)), axis = 0)
            ar = np.append(ar, df_ar, axis=0)