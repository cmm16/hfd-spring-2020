from os.path import join, dirname
import pandas as pd
from os import getcwd, mkdir

import time_eda
import race_eda
# each helper file should have one or two functions that you call here those

incidents_df = pd.read_csv("test/imagetrend_incidents.csv")
train_df = pd.read_csv("test/final_train_categories.csv")

def main(output_dir):
    # mkdir(output_dir)

    # time_eda.run_time_eda(output_dir, incidents_df) 
    race_eda.run_race_eda(output_dir, train_df)

    # run_race_eda()
    print("hello")

    # I can use data dir arguement to access any piece of data I want by using join
    print("data dir:", output_dir)
    #path_to_some_data = join(data_dir, "some_data")


if __name__ == '__main__':
    main(join(dirname(dirname(getcwd())), "eda_output"))