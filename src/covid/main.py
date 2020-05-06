from os.path import join, dirname
from os import getcwd, mkdir
import pandas as pd 

import time_eda
import clustering
import call_prob
import final_labels

### Sample file paths ### 
incidents =  pd.read_csv("test/imagetrend_incidents.csv")
data = pd.read_csv("test/covid_indices.csv")
bg_filepath = 'test/Census_FIP12_within_Fire_Dis.geojson'

def main(output_dir):
	mkdir(output_dir)

	time_eda.run(output_dir, incidents)
	clustered_df = clustering.run(output_dir, data, bg_filepath)
	all_labelled = call_prob.run(output_dir, clustered_df)
	final_labels.run(output_dir, all_labelled, bg_filepath)

if __name__ == "__main__":
    main(join(dirname(dirname(getcwd())), "covid_output"))