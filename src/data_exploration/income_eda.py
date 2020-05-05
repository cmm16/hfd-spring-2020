import pandas as pd
from os.path import join
import general_eda 

def run_income_eda(output_dir, train_df): 
	"""
	This function runs the income portion of EDA. 

	Input: 
		- output_dir: String path to output directory 
		- train_df: Dataframe of census and call counts per block group 
	"""
	# Data wrangling and preparation 
	avgs, portions = general_eda.get_quantile_data('medHHinc', train_df)
	avgs.to_csv(join(output_dir, "income_call_category_averages.csv"))
	# Chi-squared test 
	general_eda.chi_squared_test(output_dir, avgs, "Income")
	# Make plots
	general_eda.plot_quartiles(output_dir, train_df, 'medHHinc', "Median Household Income")
	general_eda.plot_call_dist(output_dir, portions, "Income Quartiles", ['Lower', 'Lower Middle', 'Upper Middle', 'Middle'], "Income")
