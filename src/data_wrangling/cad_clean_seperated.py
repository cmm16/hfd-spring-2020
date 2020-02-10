import pandas as pd
from os import path
from os import getcwd


def format_date_time(csv_file):
    """
    """
    dat = pd.read_csv(csv_file)

    # The third column represents Departure Date of the Unit
    # The format output by clean_inc_unit is "YYYYMMDD"
    dat[["3"]] = dat[["3"]].astype(str)
    ymdDF = dat['3'].str.extract('(.{4})(.{2})(.{2})')
    ymdDF = ymdDF.rename(columns={0: "Dep_Year", 1: "Dep_Month", 2: "Dep_Day"})
    dat = pd.concat([dat, ymdDF], axis=1, sort=False)

    # Arrival Dates
    dat[["5"]] = dat[["5"]].astype(str)
    ymdDF_arr = dat['5'].str.extract('(.{4})(.{2})(.{2})')
    ymdDF_arr = ymdDF_arr.rename(columns={0: "Arr_Year", 1: "Arr_Month", 2: "Arr_Day"})
    dat = pd.concat([dat, ymdDF_arr], axis=1, sort=False)

    # Departure Times
    dep_timeDF = dat['4'].str.split(':', 2, expand=True)
    dep_timeDF = dep_timeDF.rename(columns={0: "Dep_Hour", 1: "Dep_Minute", 2: "Dep_Second"})
    dat = pd.concat([dat, dep_timeDF], axis=1, sort=False)

    # Arrival Times
    arr_timeDF = dat['6'].str.split(':', 2, expand=True)
    arr_timeDF = arr_timeDF.rename(columns={0: "Arr_Hour", 1: "Arr_Minute", 2: "Arr_Second"})
    dat = pd.concat([dat, arr_timeDF], axis=1, sort=False)

    # Drop the Redundant Columns
    dat = dat.drop('3', 1)
    dat = dat.drop('4', 1)
    dat = dat.drop('5', 1)
    dat = dat.drop('6', 1)

    return dat


def save_formatted_cad_data(df, directory):
    """
    :param df:
    :param directory:
    :return:
    """
    df.to_csv(directory)


def main():

    # Get into your Data Director
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")

    # Pull clean_cad.csv
    formatted_csv = path.join(data_dir, "clean_cad.csv")

    # Format clean_cad.csv
    formatted_data = format_date_time(formatted_csv)

    # directory to cave
    save_directory = path.join(data_dir, "formatted_clean_cad.csv")
    save_formatted_cad_data(formatted_data, save_directory)


if __name__ == '__main__':
    main()
