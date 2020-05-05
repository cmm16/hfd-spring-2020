import pandas as pd
from os.path import join
import general_eda 

def run_age_eda(output_dir, train_df): 
	"""
	This function runs the age portion of EDA. 

	Input: 
		- output_dir: String path to output directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	Output: 
		- single column data frame of data  
	"""
	portions_df, train_df = data_wrangling(train_df)
	general_eda.plot_quartiles(output_dir, train_df, 'avgAge', "Weighted Average Age")
	general_eda.plot_call_dist(output_dir, portions_df, "Age", ['Youngest', 'Middle Younger', 'Middle Older', 'Oldest'])

def data_wrangling(data):
	"""
	This function prepares the data for age wrangling. First, the function adds 'avgAge',
	which is the weighted average age for the block group, to the dataframe passed in. 
	Then the function creates a table of proportions for each quartile. 

	Input: 
		- data: train_categories dataframe 

	Output: 
		- dataframe of call category proportion per quartile  
		- modified input dataframe with 'avgAge' column
	"""
	data['avgAge'] = data['pctAge0004']/100*2 + data['pctAge0017']/100*10.5 + data['pctAdult1829']/100*23.5 + data['pctAdult3044']/100*37 + data['pctAdult4564']/100*54.5 + data['pctAdult65p']/100*72.5
	portions = general_eda.make_quartile_proportions('avgAge', data)
	return portions, data 



