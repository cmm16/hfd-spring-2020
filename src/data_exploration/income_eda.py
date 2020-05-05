import pandas as pd
from os.path import join
import general_eda 

def run_income_eda(output_dir, train_df): 
	"""
	This function runs the income portion of EDA. 

	Input: 
		- output_dir: String path to output directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	Output: 
		- single column data frame of data  
	"""
	# Data wrangling and preparation 
	avgs, portions = general_eda.get_quantile_data('medHHinc', train_df)
	avgs.to_csv(join(output_dir, "income_call_category_averages.csv"))
	# Make plots
	general_eda.plot_quartiles(output_dir, train_df, 'medHHinc', "Median Household Income")
	general_eda.plot_call_dist(output_dir, portions, "Income", ['Lower', 'Lower Middle', 'Upper Middle', 'Middle'])


