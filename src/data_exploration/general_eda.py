import pandas as pd 
from os.path import join
import numpy as np
import matplotlib.pyplot as plt

def make_quartile_proportions(column, data):
	"""
	This function creates a matrix of the propotion of calls for each quartile
	in a given column. 

	Input: 
		- column: String name of column
		- data: train_categories dataframe 
	
	Output: 
		- dataframe of call proportions for each quartile 
	""" 
	q25 = data[column].quantile(.25)
	q50 = data[column].quantile(.5)
	q75 = data[column].quantile(.75)
	# Create subset of each quartile 
	q1df = data[data[column] <= q25]
	q2df = data[(data[column] > q25) & (data[column] <= q50)]
	q3df = data[(data[column] > q50) & (data[column] <= q75)]
	q4df = data[data[column] > q75]
	# Get average number of calls of each type
	q1_mean = q1df[['health','injuries_external','mental_illness', 'motor', 'fire', 'other']].mean()
	q2_mean = q2df[['health','injuries_external','mental_illness', 'motor', 'fire', 'other']].mean()
	q3_mean = q3df[['health','injuries_external','mental_illness', 'motor', 'fire', 'other']].mean()
	q4_mean = q4df[['health','injuries_external','mental_illness', 'motor', 'fire', 'other']].mean()
	# Make dataframe of averages 
	avgs = pd.DataFrame([q1_mean, q2_mean, q3_mean, q4_mean])
	# Convert to proportions
	portions = avgs.apply(lambda row: row/row.sum(), axis=1)
	portions['quartile'] = ""
	portions.at[0, 'ageRange'] = "Lowest"
	portions.at[1, 'ageRange'] = "Middle-Lowest"
	portions.at[2, 'ageRange'] = "Middle-Upper"
	portions.at[3, 'ageRange'] = "Highest"
	return portions 


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


def EMSvsFireBarPlot(data, title="Daily Calls", day = True): 
	"""
	Plots the proportion of calls that are EMS vs. Fire 

	Input: 
	- data dataframe of imagetrend data containing column 'EMS_or_Fire_Event'
		with either 'EMS' or 'FIRE' value. 
	-day: true for daily level of granularity, false for monthly level 
	- title: string name of title of plot 
	"""
	ems = data[data['EMS_or_Fire_Event'] == 'EMS']
	fire = data[data['EMS_or_Fire_Event'] == 'FIRE']	
	if (granularity):
		plotems = plt.hist(ems.Date, 31, alpha=.6, edgecolor = 'black',  linewidth=1)
		plotfire = plt.hist(fire.Date, 31, alpha=.8, edgecolor = 'black',  linewidth=1)	
		plt.xlabel('Day')
	else: 
		plotems = plt.hist(ems.Month, 12, alpha=.6, edgecolor = 'black',  linewidth=1)
		plotfire = plt.hist(fire.Month, 12, alpha=.8, edgecolor = 'black',  linewidth=1)	
		plt.xlabel('Month')
	plt.title(title)
	plt.legend(['ems', 'fire'])
	plt.ylabel('Call Count')
	plt.show()

def callDistGroupedBarPlot(df, legend_labels): 
	"""
	Plots number of calls of each call category for different groupings. 
	(ex: plot number of calls of each call category for different clusters)

	Input: 
	- df: dataframe where rows are call category and columns are groupings. 
	- legend_labels: list of string labels for each grouping 

	Output: grouped bar chart of number of calls for each category 
	"""
	df.plot.bar()
	plt.legend(legend_labels)
	plt.title("Cluster Call Distribution")
	plt.ylabel("Number of Calls per Block Group")
	plt.xlabel("Call Category")
	plt.show()

def callProportionStackedBar(df, xlabel="Groupings"): 
	"""
	Creates a stacked bar chart (in fire color scheme) of the proportion of calls of 
	each call category for each grouping. 

	Input: 
	- df: dataframe of percentages of each call category, where call categories 
		are the columns and groupings are the rows
	- xlabel: string describing the types of groupings made

	Output: stacked bar chart with proportion of each call category for a grouping 
	"""
	fig = plt.figure()
	ax = fig.add_subplot(111)
	callsPercent.plot(ax=ax, kind='bar', stacked=True, rot=0, color=['coral', 'red', 'yellow', 'darkorange', 'firebrick', 'gold'])
	plt.title("Call Distribution", fontsize=20)
	plt.ylabel("Portion of Calls", fontsize=18)
	plt.yticks(fontsize=15)
	plt.xlabel(xlabel, fontsize=18)
	plt.show()


