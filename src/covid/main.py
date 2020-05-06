from os.path import join, dirname
from os import getcwd, mkdir
import pandas as pd 

import time_eda
import clustering
import call_prob
import final_labels
import fire_dist

### Sample file paths ### 
# incidents =  pd.read_csv("test/imagetrend_incidents.csv")
# bg_data = pd.read_csv("test/covid_indices.csv")
# fd_data = pd.read_csv("test/firedist_covid2.csv")
# bg_filepath = 'test/Census_FIP12_within_Fire_Dis.geojson'
# fd_filepath = 'test/fire_districts.geojson'

# def main(output_dir, incidents, bg_data, fd_data, bg_filepath, fd_filepath):
def main(output_dir):
	mkdir(output_dir)

	### BLOCK GROUP FUNCTIONS ### 
	time_eda.run(output_dir, incidents)
	clustered_df = clustering.run(output_dir, bg_data, bg_filepath)
	all_labelled = call_prob.run(output_dir, clustered_df)
	final_labels.run(output_dir, all_labelled, bg_filepath)

	### FIRE DISTRICT FUNCTIONS ### 
	fire_dist.run(output_dir, fd_data, fd_filepath)

if __name__ == "__main__":
    main(join(dirname(dirname(getcwd())), "covid_output"))
    # incidents, bg_data, fd_data, bg_filepath, fd_filepath


