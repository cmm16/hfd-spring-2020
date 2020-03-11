import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime
from datetime import datetime

def data_wrangle(df, level="Day", year=2011):
	"""
	This function prepares the data for analysis. The function first drops all 
	calls from 2011 (or user input year), because that is the year with incomplete 
	records. Then, the data is counted by day or month depending on user input. 
	If count by month, data is standardized to the number of days in a month.
	The counted data is then unstacked and flattened into a single numpy array and 
	dataframe. 

	Input: 
		- df: Dataframe with columns "Incident_ID", Year", "Month", "Date" (optional)
		- level: String specifying level to analyze data 
		- year: Integer specifying year to drop data of 

	Returns: 
		- a one dimension numpy array of the data 
		- a single column data frame of the data 
	"""
	# Drop all entries from 2011 
	df = df[df['Year']!=year] 
	if level == "Month": 
		raw_groupBy = df.groupby(['Year','Month']).count()['Incident_ID'].unstack(0)
		num_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		groupBy = raw_groupBy.apply(lambda x: x / num_day, axis =0)
	else: 
		groupBy = df.groupby(['Year','Month','Date']).count()['Incident_ID'].unstack(0)
	all_data = groupBy.values.flatten(order='F')
	data = all_data[~np.isnan(all_data)]
	timedf = pd.DataFrame(data)
	return data, timedf

def plot_raw_data(data, base_unit="day"):
	"""
	This function plots a time series. 
	Data can be of two levels: daily and monthly. If data is daily, 
	then plot will include Harvey regions. Otherwise, returns a monthly plot. 

	Input: 
		- data: single column data frame 
		- base_unit: String specifying granularity of data 
	"""
    data.plot(figsize=(10,8))
    plt.title("Number of Calls from 1/2012 - 12/2017")
    plt.ylabel('Call Count')
    plt.xlabel('Year')
    # Determine whether data is yearly or monthly 
    if base_unit == "monthly": 
    	plt.xticks([0, 12, 24, 36, 48, 60, 72], [2012, 2013, 2014, 2015, 2016, 2017]) 
    else: 
        plt.xticks([0, 366, 731, 1096, 1461, 1827, 2192], [2012, 2013, 2014, 2015, 2016, 2017])
        plt.axvline(x=229 + 365*5, ls='dashed', color='red') # August 17, 2017 
        plt.axvline(x=254 + 365*5, ls='dashed', color='red') # September 12, 2017 
    	plt.legend(["Counts", "Harvey"])
    plt.show()

def dicky_fuller_test(data): 
	"""
	Function that tests a series for stationarity using the Dickey-Fuller Test. 

	Input: single column data frame 
	"""
	print('Results of Dickey-Fuller Test:')
	result = adfuller(timedf)
	print('> ADF Statistic: {:.3f}'.format(result[0]))
	print('> p-value: {:.3e}'.format(result[1]))
	print('> Critical Values:')
	for key, value in result[4].items():
	    print('\t%s: %.3f' % (key, value))


def rolling_plots(timeseries, rolling=24):
	"""
	Function that creates rolling window plots. 

	Input: 
		- timeseries: single column data frame 
		- rolling: Integer size of window
	"""   

    #Determing rolling statistics
    rolmean = timeseries.rolling(window = rolling).mean()
    rolstd = timeseries.rolling(window = rolling).std()
    
    #Plot rolling statistics:
    plt.figure(figsize=(10,5))
    orig = plt.plot(timeseries, color='darkgray',label='Original')
    mean = plt.plot(rolmean, color='darkblue', label='Rolling Mean', lw=1)
    std = plt.plot(rolstd, color='red', label = 'Rolling Std', lw=1)
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.ylabel('Call Count')
    plt.xlabel('Year')
    plt.xticks([0, 366, 731, 1096, 1461, 1827, 2192], [2012, 2013, 2014, 2015, 2016, 2017])
    plt.xlim(timeseries.index.min(), timeseries.index.max())
    plt.show(block=False)
    return rolmean, rolstd


def plot_acf_pacf(timeseries, title): 
	"""
	Function that creates ACF/PACF for given data

	Input: 
		- timseries: single column data frame
		- title: String specifying type of data and will be appended to title 
	"""
    plot_acf(timeseries)
    plt.title(title+" Autocorrelation")
    plt.ylabel("ACF Value")
    plt.xlabel("Lag")
    plot_pacf(timeseries)
    plt.title(title+" Partial Autocorrelation")
    plt.ylabel("PACF Value")
    plt.xlabel("Lag")
    plt.show()

