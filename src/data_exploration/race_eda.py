import pandas as pd
from os.path import join
import numpy as np 
import matplotlib.pyplot as plt

import general_eda
import mapping 

def run_race_eda(output_dir, train_df): 
	"""
	This function runs the race portion of EDA, and will generate 
	a donut chart of race, map, call volume, and call proportion plot. 

	Input: 
		- data_dir: String path to data directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	Output: 
		- single column data frame of data  
	"""
	races = ['White', 'Hispanic', 'Black', 'Asian']
	sizes, race_avgs, train = data_wrangling(train_df)
	race_avgs.to_csv(join(output_dir, "race_call_category_averages.csv"))
	
	# Chi-squared test 
	general_eda.chi_squared_test(output_dir, race_avgs, "Race")

	# Volume chart 
	general_eda.plot_volume_chart(output_dir, race_avgs, "Average Calls per Racially Homogeneous Block Groups", 
		"Homogeneous Race", [0,1,2,3], races)
	
	# Create portion donut chart 
	labels=['White', 'Hispanic', 'Black', 'Asian', 'Heterogenous'] 
	general_eda.plot_donut_chart(output_dir, sizes, labels, "race")

	# Convert to proportions
	call_cols = ['health','injuries_external','mental_illness', 'motor', 'fire', 'other']
	portions = race_avgs[call_cols].apply(lambda row: row/row.sum(), axis=1)
	general_eda.plot_call_dist(output_dir, portions, "Race", races, "Race")


def data_wrangling(train): 
	train = general_eda.calculate_total_calls(train)
	# Split data into majority race dataframes 
	white_blocks = train[train['pctNHwht'] >= 50]
	hisp_blocks = train[train['pctHisp'] >= 50]
	blk_blocks = train[train['pctNHblk'] >= 50]
	asian_blocks = train[train['pctNHasi'] >= 50]

	# Tag original data with racial majority 
	train["race_value"] = 0
	train.loc[train.pctNHwht >= 50, 'race_value'] = 1	# white 
	train.loc[train.pctHisp >= 50, 'race_value'] = 2	# hispanic
	train.loc[train.pctNHblk >= 50, 'race_value'] = 3	# black 
	train.loc[train.pctNHasi >= 50, 'race_value'] = 4	# asian 

	# Get sizes of each majority block group 
	sizes = [white_blocks.shape[0], hisp_blocks.shape[0], blk_blocks.shape[0], asian_blocks.shape[0]]
	no_majority = len(train) - sum(sizes) 
	sizes.append(no_majority)

	# Calculate average of each type 
	columns = ['health','injuries_external','mental_illness', 'motor', 'fire', 'other', 'total_calls', 'total_calls_per_cap']
	white_blocks_avg = white_blocks[columns].mean() 
	hisp_blocks_avg = hisp_blocks[columns].mean()  
	blk_blocks_avg = blk_blocks[columns].mean()
	asian_blocks_avg = asian_blocks[columns].mean()
	race_avgs = pd.DataFrame([white_blocks_avg, hisp_blocks_avg, blk_blocks_avg, asian_blocks_avg])
	
	return sizes, race_avgs, train 

