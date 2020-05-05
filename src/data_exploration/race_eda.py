import pandas as pd
from os.path import join
import numpy as np 
import matplotlib.pyplot as plt

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
	# Split data into majority race dataframes 
	train['TotalCalls'] = train['health'] + train['injuries_external'] + train['mental_illness'] + train['morow']
	white_blocks = train[train['pctNHwht'] >= 50]
	hisp_blocks = train[train['pctHisp'] >= 50]
	blk_blocks = train[train['pctNHblk'] >= 50]
	asian_blocks = train[train['pctNHasi'] >= 50]

	white_blocks = white_blocks[interest_cols]

	interest_cols = ["TotalPop", 'health','injuries_external','mental_illness', 'motor', 'fire', 'other']

	# Create portion donut chart 

def plot_race_proportions(): 
	plt.rcParams['figure.figsize'] = [10, 10] # controls figure size
	names='White', 'Hispanic', 'Black', 'Asian', 'Heterogenous'
	size=[len(white_blocks), len(hisp_blocks), len(blk_blocks), len(asian_blocks), no_majority]
	 
	# Create a circle for the center of the plot
	my_circle=plt.Circle((0,0), 0.7, color='white')

	# Give color names
	plt.pie(size, labels=names, colors=['darkorange','red','coral','firebrick','gold']) # fire themed
	p=plt.gcf()
	p.gca().add_artist(my_circle)

	plt.savefig(join(output_dir, "race_donut_chart.png"))


# train_df = pd.read_csv("test/final_train_categories.csv")

