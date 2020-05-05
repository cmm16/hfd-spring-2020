import pandas as pd 
from os.path import join
import numpy as np
import matplotlib.pyplot as plt

def get_quantile_data(column, data):
	"""
	This function creates a matrix of the propotion of calls for each quartile
	in a given column. 

	Input: 
		- column: String name of column
		- data: train_categories dataframe 
	
	Output: 
		- dataframe of call proportions for each quartile 
	""" 
	# Calculate total number of calls 
	call_cols = ['health','injuries_external','mental_illness', 'motor', 'fire', 'other']
	data['total_calls'] = 0
	for call in call_cols: 
		data['total_calls'] += data[call]
	# Standardize per capita 
	data['total_calls_per_cap'] =  data['total_calls']/data['TotalPop']
	# Calculate quantiles 
	q25 = data[column].quantile(.25)
	q50 = data[column].quantile(.5)
	q75 = data[column].quantile(.75)
	# Create subset of each quartile 
	q1df = data[data[column] <= q25]
	q2df = data[(data[column] > q25) & (data[column] <= q50)]
	q3df = data[(data[column] > q50) & (data[column] <= q75)]
	q4df = data[data[column] > q75]
	# Get average number of calls of each type
	q1_mean = q1df[call_cols+['total_calls', 'total_calls_per_cap']].mean()
	q2_mean = q2df[call_cols+['total_calls', 'total_calls_per_cap']].mean()
	q3_mean = q3df[call_cols+['total_calls', 'total_calls_per_cap']].mean()
	q4_mean = q4df[call_cols+['total_calls', 'total_calls_per_cap']].mean()
	# Make dataframe of averages 
	avgs = pd.DataFrame([q1_mean, q2_mean, q3_mean, q4_mean])
	# Convert to proportions
	portions = avgs[call_cols].apply(lambda row: row/row.sum(), axis=1)
	portions['quartile'] = ""
	portions.at[0, 'quartile'] = "Lowest"
	portions.at[1, 'quartile'] = "Middle-Lowest"
	portions.at[2, 'quartile'] = "Middle-Upper"
	portions.at[3, 'quartile'] = "Highest"
	return avgs, portions 


def plot_quartiles(output_dir, data, column, column_name): 
	"""
	This function creates a histogram of a given column with a line at the 
	25, 50, and 75 quartiles. 

	Inputs: 
		- output_dir: String path to output directory
		- column: String name of column in dataframe 
		- data: train_categories dataframe 
		- column_name: String name of column for display purposes
	"""
	plt.figure(figsize=(12,8))
	data[column].hist(bins=100)
	# Get quartiles and add as line 
	q25 = data[column].quantile(.25)
	q50 = data[column].quantile(.5)
	q75 = data[column].quantile(.75)
	plt.plot([q25, q25], [0, 500], linewidth=3)
	plt.plot([q50, q50], [0, 500], linewidth=3)
	plt.plot([q75, q75], [0, 500], linewidth=3)
	plt.ylim(0, 55)

	# Plot attributes 
	plt.title(column_name+" Distribution", fontsize=20)
	plt.ylabel("Number of Block Groups", fontsize=18)
	plt.yticks(fontsize=15)
	plt.xlabel(column_name, fontsize=18)
	plt.xticks(fontsize=15)
	plt.legend(['25th Quartile','50th Quartile','75th Quartile'])
	plt.savefig(join(output_dir, column_name+"_quartiles.png"))

def plot_call_dist(output_dir, portions_df, column_name, labels): 
	"""
	This function creates a stacked bar chart of the call proportions 
	for each quantile.  

	Input: 

	"""
	callLabels = ["Health (internal)", "External Injuries", "Mental Illness", "Motor", 'Fire', 'Other']
	fig = plt.figure(figsize=(20,15))
	ax = fig.add_subplot(111)
	portions_df.plot(ax=ax,kind='bar', stacked=True, rot=0, color=['coral', 'red', 'yellow', 'darkorange', 'firebrick', 'gold'])
	plt.title("Call Distribution", fontsize=20)
	plt.ylabel("Proportion of Calls", fontsize=18)
	plt.yticks(fontsize=15)
	plt.xlabel(column_name+" Quantile", fontsize=18)
	plt.legend(prop={'size': 20}, labels=callLabels)
	plt.xticks(ticks=[0,1, 2, 3],labels=labels, fontsize=15)
	plt.savefig(join(output_dir, column_name+"_call_dist.png"))




