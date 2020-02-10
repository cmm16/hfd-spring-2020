import pandas as pd
from os import path
from os import getcwd
import time


def transit_calc(row):
    """
    Assumptions - Arrival time is always after departure time
    """
    # Most case: Departure time is 2:58 and Arrival Time is 4:01
    if int(row['Dep_Hour']) <= int(row['Arr_Hour']):
        diff = int(row['Arr_Hour']) - int(row['Dep_Hour'])

        if diff == 0:
            # For Instance, Departure time was 3:28 and Arrival Time was 3:58
            val = int(row['Arr_Minute']) - int(row['Dep_Minute'])

        elif diff == 1:
            # For Instance, Departure time was 3:50 and Arrival Time was 4:01
            val = 60 - (int(row['Dep_Minute'])) + int(row['Arr_Minute'])

        else:
            # For instance, Departure time was 3:59 and Arrival Time was 5:03
            val = 60 - (int(row['Dep_Minute'])) + int(row['Arr_Minute']) + 60 * (diff - 1)

    # Pathological Case : Departure time is at 23:50 and Arrival time is 00:30
    else:

        time_until_midnight = 60 * (24 - int(row['Dep_Hour']) - 1) + 60 - int(row['Dep_Minute'])
        time_after_midnight = 60 * int(row['Arr_Hour']) + int(row['Arr_Minute'])
        val = time_until_midnight + time_after_midnight
    return val


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

    # Rename the columns that categorize station_id,  unit_ID, and incident_id
    dat = dat.rename(columns={'0': "Incident_ID", '1': 'Unit_ID', '2': "Station_ID"})

    # Drop the Redundant Columns
    dat = dat.drop('3', 1)
    dat = dat.drop('4', 1)
    dat = dat.drop('5', 1)
    dat = dat.drop('6', 1)
    dat = dat.drop('Unnamed: 0', 1)  # Some index column

    # Calculate Transit Times - runtime is about 4 minutes
    dat.is_copy = False  # pd.options.mode.chained_assignment = None is another option
    dat['Transit_Time'] = dat.apply(transit_calc, axis=1)

    return dat


def save_formatted_cad_data(df, directory):
    """
    :param df:
    :param directory:
    :return:
    """
    df.to_csv(directory)


def main():
    # Runtime of main() is --- 290.41543197631836 seconds ---
    # Get into your Data Director
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")

    # Pull clean_cad.csv
    formatted_csv = path.join(data_dir, "clean_cad.csv")

    # Format clean_cad.csv
    formatted_data = format_date_time(formatted_csv)

    # directory to save
    save_directory = path.join(data_dir, "formatted_clean_cad.csv")
    save_formatted_cad_data(formatted_data, save_directory)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
