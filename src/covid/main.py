from os.path import join, dirname
from os import getcwd, mkdir
import pandas as pd 

import time_eda
import clustering

incidents =  pd.read_csv("test/imagetrend_incidents.csv")
data = pd.read_csv("test/final_train_categories.csv")

def main(output_dir):
	# mkdir(output_dir)

	# time_eda.run(output_dir, incidents)
	clustered_df = clustering.run(output_dir, data)
	all_

if __name__ == "__main__":
    main(join(dirname(dirname(getcwd())), "covid_output"))