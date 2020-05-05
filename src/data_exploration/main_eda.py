from os.path import join, dirname
import pandas as pd
from os import getcwd, mkdir
# you should import all helper files here
import time_series as time_eda
# each helper file should have one or two functions that you call here those

incidents_df = pd.read_csv("test/imagetrend_incidents.csv")

def main(output_dir):
    mkdir(output_dir)

    # data dir will be set to any users Data directory if they put it at the top level of the project
    time_eda.run_time_eda(output_dir, incidents_df) 

    # run_race_eda()
    print("hello")

    # I can use data dir arguement to access any piece of data I want by using join
    print("data dir:", output_dir)
    #path_to_some_data = join(data_dir, "some_data")


if __name__ == '__main__':
    main(join(dirname(dirname(getcwd())), "eda_output"))