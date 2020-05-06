import pandas as pd
import numpy as np
from os import listdir
from os import path
from os import getcwd
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
            with ZipFile(path_to_zip, "r") as zipObj:
                # will place all unzipped files in save_directory, will write over the old files so creating
                # duplicates by running function multiple times is not possible
                zipObj.extractall(save_directory)


def merge_csvs(directory, inc_type="inc"):
    """
    Merges all the csvs in a target directory with a certain naming convention return result as a single numpy array

    Arguments:
        directory (str): String path to directory with csvs to be merged
        inc_type (str): String that should be "inc" or "unit" depending on the cad data to be merged

    Returns:
        (numpy array): Numpy array that is the values of all the merged csvs
    """
    # place holder array
    ar = np.ndarray((0, 6))

    for file in listdir(directory):
        path_to_csv = path.join(directory, file)

        # logic statement to differentiate incident and incident unit based on input
        if inc_type == "inc" and file.startswith("c:franknHFD"):
            df_ar = read_sql_csv(path_to_csv)
            ar = np.append(ar, df_ar, axis=0)
        elif inc_type == "unit" and not file.startswith("c:franknHFD"):
            df_ar = read_sql_csv(path_to_csv)
            ar = np.append(ar, df_ar, axis=0)
    return ar


def read_sql_csv(path_to_csv):
    """
    Given a path to a csv generated using sql will read this csv and return it as a numpy array

    Arguments:
        path_to_csv (str): String path to csv generated using sql

    Returns:
        (numpy array): Numpy array not containing extra sql garbage
    """
    file = open(path_to_csv, "r")
    first_line = file.readline()

    # logic to determine how many lines should be skipped based off of extra sql
    if len(first_line) == 6:
        # skip first two lines since these are sql garbage, will make first actual row into column names
        df = pd.read_csv(path_to_csv, skiprows=2, low_memory=False)
    elif len(first_line) == 7:
        # skip first line since this is sql garbage, will make first actual row into column names
        df = pd.read_csv(path_to_csv, skiprows=1, low_memory=False)
    else:
        return np.ndarray((0, 6))

    # take df values and remove two last lines that are sql garbage
    df_values = np.delete(df.values, [len(df.values) - 1, len(df.values) - 2], axis=0)
    # add column names to values since these are actually the first valid row
    first_valid_row = df.columns.values.reshape((1, 6))
    df_ar = np.append(df_values, np.reshape(first_valid_row, (1, 6)), axis=0)
    return df_ar


def clean_unit(ar):
    """
    Cleans and formats incident unit data numpy array

    Arguments:
        ar (numpy array): Numpy array of incident unit data from merge_csvs

    Returns:
        (numpy aarray): Numpy array cleaned of incident unit data
    """
    # change to pass back df
    # add naming and other cleaning function from ehmres code

    merged_df = pd.DataFrame(ar)
    # split the two columns that have space as their delimiter instead of comma
    split_df1 = merged_df[4].str[1:-1].str.split(" ", expand=True)
    split_df2 = merged_df[5].str[1:-1].str.split(" ", expand=True)

    # Rename the columns that categorize station_id,  unit_ID, and incident_id
    merged_df = merged_df.rename(
        columns={0: "Incident_ID", 1: "Unit_ID", 2: "Station_ID"}
    )
    split_df1 = split_df1.rename(columns={0: "dep_date", 1: "dep_time"})
    split_df2 = split_df2.rename(columns={0: "arrival_date", 1: "arrival_time"})
    merged_df = pd.concat(
        [merged_df[["Incident_ID", "Unit_ID", "Station_ID"]], split_df1, split_df2],
        axis=1,
    )

    # The third column represents Departure Date of the Unit
    # The format output by clean_inc_unit is "YYYYMMDD"
    merged_df[["dep_date"]] = merged_df[["dep_date"]].astype(str)
    ymdDF = merged_df["dep_date"].str.extract("(.{4})(.{2})(.{2})")
    ymdDF = ymdDF.rename(columns={0: "Dep_Year", 1: "Dep_Month", 2: "Dep_Day"})
    merged_df = pd.concat([merged_df, ymdDF], axis=1, sort=False)

    # Arrival Dates
    merged_df[["arrival_date"]] = merged_df[["arrival_date"]].astype(str)
    ymdDF_arr = merged_df["arrival_date"].str.extract("(.{4})(.{2})(.{2})")
    ymdDF_arr = ymdDF_arr.rename(columns={0: "Arr_Year", 1: "Arr_Month", 2: "Arr_Day"})
    merged_df = pd.concat([merged_df, ymdDF_arr], axis=1, sort=False)

    # Departure Times
    dep_timeDF = merged_df["dep_time"].str.split(":", 2, expand=True)
    dep_timeDF = dep_timeDF.rename(
        columns={0: "Dep_Hour", 1: "Dep_Minute", 2: "Dep_Second"}
    )
    merged_df = pd.concat([merged_df, dep_timeDF], axis=1, sort=False)

    # Arrival Times
    arr_timeDF = merged_df["arrival_time"].str.split(":", 2, expand=True)
    arr_timeDF = arr_timeDF.rename(
        columns={0: "Arr_Hour", 1: "Arr_Minute", 2: "Arr_Second"}
    )
    merged_df = pd.concat([merged_df, arr_timeDF], axis=1, sort=False)

    # Drop the Redundant Columns
    merged_df = merged_df.drop("dep_date", 1)
    merged_df = merged_df.drop("dep_time", 1)
    merged_df = merged_df.drop("arrival_date", 1)
    merged_df = merged_df.drop("arrival_time", 1)

    merged_df.is_copy = (
        False  # pd.options.mode.chained_assignment = None is another option
    )
    merged_df["Transit_Time"] = merged_df.apply(transit_calc, axis=1)

    return merged_df


def transit_calc(row):
    """
    Assumptions - Arrival time is always after departure time

    Arguments:
        Row : A row of a pandas data frame

    Returns:
        val : A integer that represents transit time

    """
    # Most case: Departure time is 2:58 and Arrival Time is 4:01
    if int(row["Dep_Hour"]) <= int(row["Arr_Hour"]):
        diff = int(row["Arr_Hour"]) - int(row["Dep_Hour"])

        if diff == 0:
            # For Instance, Departure time was 3:28 and Arrival Time was 3:58
            val = int(row["Arr_Minute"]) - int(row["Dep_Minute"])

        elif diff == 1:
            # For Instance, Departure time was 3:50 and Arrival Time was 4:01
            val = 60 - (int(row["Dep_Minute"])) + int(row["Arr_Minute"])

        else:
            # For instance, Departure time was 3:59 and Arrival Time was 5:03
            val = (
                60 - (int(row["Dep_Minute"])) + int(row["Arr_Minute"]) + 60 * (diff - 1)
            )

    # Pathological Case : Departure time is at 23:50 and Arrival time is 00:30
    else:

        time_until_midnight = (
            60 * (24 - int(row["Dep_Hour"]) - 1) + 60 - int(row["Dep_Minute"])
        )
        time_after_midnight = 60 * int(row["Arr_Hour"]) + int(row["Arr_Minute"])
        val = time_until_midnight + time_after_midnight
    return val


def clean_inc(ar):
    """
    Cleans the incident

    Arguments:
        ar (numpy array): A numpy array of incident data

    Returns:
        A clean data frame
    """
    # change to pass back df
    # add naming and other cleaning function from emhres code

    merged_df = pd.DataFrame(ar)

    # remove extraneous "'" signs
    merged_df[2] = merged_df[2].str[1:]
    merged_df[3] = merged_df[3].str[:-1]
    merged_df[4] = merged_df[4].str[1:-1]
    merged_df[5] = merged_df[5].str[1:-1]

    # remove all entries without x, y coordinates
    merged_df = merged_df[merged_df[4] != ""]
    merged_df = merged_df[merged_df[5] != ""]
    merged_df[4] = merged_df[4].astype("int")
    merged_df[5] = merged_df[5].astype("int")

    # placing decimal place in correct position
    merged_df[4] = merged_df[4] / (10.0 ** 6)
    merged_df[5] = merged_df[5] / (10.0 ** 6)

    merged_df = merged_df.rename(
        columns={
            0: "Incident_ID",
            1: "Call_Type",
            2: "Address",
            3: "City_ID",
            4: "Longitude",
            5: "Latitude",
        }
    )

    # We then merge it with the call types xlsx file and reformat to be usable for
    #     data exploration.
    data_dir = path.join(path.dirname(getcwd()), "data")
    call_data = path.join(data_dir, "CAD Call Types - ImageTrend values.xlsx")

    call_df = pd.read_excel(
        call_data
    )  # This is an excel file that has the call type codes and descriptions

    call_df = call_df.rename(
        columns={
            "TYPE": "Call_Type",
            "DESCRIPTION": "Description",
            "DEFAULT PRIOITY": "Default_Priority",
        }
    )  # Rename columns for Merging and for Standard Naming Procedures

    formatted_merged_df = pd.merge(
        merged_df, call_df, on="Call_Type"
    )  # Merge on Key Call_Type

    return formatted_merged_df


def cad_wrangling(directory, save_path, inc_type="inc", unzip=True):
    """
    Runs all functions needed to wrangle the cad incident unit data given a target data base directory

    Arguments:
        directory (str): String path to the data folder
        save_path (str): String path to save location
        inc_type (str): String that should be "inc" or "unit" depending on the cad data to be merged
        unzip (bool): Boolean whether input data needs to be unziped or nnot
    """

    if unzip:
        zip_cad_path = path.join(directory, "UPDATE CAD DATA/")
        data_path = path.join(directory, "unzip_cad")
        unzip_folders(zip_cad_path, data_path)

    else:
        data_path = directory

    if inc_type=="inc":
        inc_ar = merge_csvs(data_path, "inc")
        inc_clean_ar = clean_inc(inc_ar)
        inc_clean_ar.to_csv(save_path, index=False)

    if inc_type=="unit":
        unit_ar = merge_csvs(data_path, "unit")
        unit_clean_ar = clean_unit(unit_ar)
        unit_clean_ar.to_csv(save_path, index=False)

