import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

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


