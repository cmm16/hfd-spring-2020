import pandas as pd
from os.path import join
import numpy as np 
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def run_time_eda(data_dir, incidents_df): 
	"""
	This function runs the time portion of EDA. 

	Input: 
		- data_dir: String path to data directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	Output: 
		- single column data frame of data  
	"""
	timedf = data_wrangle(incidents_df)
	plot_raw_data(data_dir, timedf)
	plot_decomposition(data_dir, timedf)


def data_wrangle(df, start_date="2013-01", level="Day"):
	"""
	This function prepares the data for analysis by counting the number of 
	incidents per day. The counted data is then unstacked and flattened into a 
	dataframe with a single column. 

	Input: 
		- df: Dataframe with columns "Event_Number", Year", "Month", "Date" (optional)
		- start_date: String indicating first day of data in "YYYY-MM" format

	Returns: 
		- array of years the data covers 
		- a single column data frame of the data 
	"""
	groupBy = df.groupby(['Year','Month','Date']).count()['Event_Number'].unstack(0)
	all_data = groupBy.values.flatten(order='F')
	flat_data = all_data[~np.isnan(all_data)]

	N = len(flat_data)
	drange = pd.date_range(start_date, periods=N)
	timedf = pd.DataFrame(flat_data, index=drange)

	return timedf

def plot_raw_data(data_dir, timedf, title="Daily Number of Calls from 1/1/2013 - 4/12/2020"):
	"""
	This function creates a time series plot and saves it to specified output directory. 

	Input: 
		- data_dir: String of path to eda outputs
		- timedf: single column data frame of daily call counts 
		- title: String title of plot
	"""
	timedf.plot(figsize=(15, 10))
	plt.title(title, fontsize=20)
	plt.xlabel("Date", fontsize=18)
	plt.xticks(fontsize=16)
	plt.ylabel("Number of Calls", fontsize=18)
	plt.yticks(fontsize=16)
	plt.savefig(join(data_dir, "timeseries.png"))

def plot_decomposition(data_dir, timedf): 
	"""
	This function creates a seasonal decomposition plot and saves it to 
	specified output directory. 

	Input: 
		- data_dir: String of path to eda outputs
		- timedf: single column data frame of daily call counts 
	"""	
	result = seasonal_decompose(timedf, model='additive',freq=365)
	plt.rcParams['figure.figsize'] = [15, 10]
	result.plot()
	plt.xlabel("Date")
	plt.savefig(join(data_dir, "timeseries_decomposition.png"))
