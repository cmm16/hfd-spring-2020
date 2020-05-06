from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import pymannkendall as mk

def run(output_dir, incidents_df):
	"""
	Creates all time-related covid-19 visualizations.

	Inputs:
		- output_dir: String path to output directory
		- incidents_df: Dataframe of ImageTrend incidents
	"""
	y20 = dataWrangling(incidents_df)
	plotTS(output_dir, y20, '3/1/2020', '4/12/2020')
	categories_df = plotCategories(output_dir, y20, '3/1/2020', '4/12/2020')
	trendTest(output_dir, categories_df)

def dataWrangling(incidents_df): 
	"""
	Subsets the data to covid-19 period.

	Inputs:
		- incidents_df: Dataframe of ImageTrend incidents

	Returns: subsetted dataframe
	"""
	# Currently contains only calls from march and april
	y20 = incidents_df[incidents_df['Year'] == 2020]
	y20 = y20[(y20['Month'] == 3) | (y20['Month'] == 4)]
	return y20

def plotTS(output_dir, data, start_date, end_date):
	"""
	Create single time series plot of daily calls.

	Inputs:
		- output_dir: String path to output directory
		- data: incident data of time period you want to graph
		- start_date: string representation of data's start date in 'M/D/YYYY' format
		- end_date: string representation of data's end date in 'M/D/YYYY' format
	"""
    counts = data.groupby(['Month','Date']).count()['Event_Number'].unstack(0)
    
    # Flatten data frame into single column
    all_data = counts.values.flatten(order='F')
    flat_data = all_data[~np.isnan(all_data)]

    # Data frame for graphing
    drange = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame(flat_data, index=drange)
    plt.rc('figure', figsize=(12, 8))

    fig, ax = plt.subplots()
    ax.plot(df.index, df.values)
    plt.title("Daily Calls", fontsize=20)
    plt.ylabel('Call Count', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.savefig(join(output_dir, "daily_calls_during_covid.png"))
    plt.close()

def makeSingle(data): 
	"""
	Flattens an incident dataframe into a single column of daily counts.

	Inputs:
		- data: dataframe of incidents

	Returns: a single array of daily counts
	"""
    counts = data.groupby(['Month','Date']).count()['Event_Number'].unstack(0)
    # Flatten data frame into single column
    all_data = counts.values.flatten(order='F')
    flat_data = all_data[~np.isnan(all_data)]
    return flat_data

def plotCategories(output_dir, data, start_date, end_date):
	"""
	Plots time series broken down into each call category.

	Inputs:
		- output_dir: String path to output directory
		- data: incident data of time period you want to graph
		- start_date: string representation of data's start date in 'M/D/YYYY' format
		- end_date: string representation of data's end date in 'M/D/YYYY' format

	Returns: dataframe of daily call counts per call category
	"""
	data["Subcall_Code"] = data["Event_Type"].str[:4]
	data["Call_Category"] = data["Subcall_Code"].apply(
		lambda x: call_category_map[x])
	motor = data[data['Call_Category']=='motor']
	m1 = makeSingle(motor)
	health = data[data['Call_Category']=='health']
	h1 = makeSingle(health)
	injuries = data[data['Call_Category']=='injuries_external']
	ie1 = makeSingle(injuries)
	other = data[data['Call_Category']=='other']
	o1 = makeSingle(other)
	mental_illness = data[data['Call_Category']=='mental_illness']
	mi1 = makeSingle(mental_illness)
	fire = data[data['Call_Category']=='fire']
	f1 = makeSingle(mental_illness)

	drange = pd.date_range(start=start_date, end=end_date)
	df = pd.DataFrame({'motor':m1, 'health': h1, 'injuries_external':ie1, 
	                   'other': o1, 'mental_illness': mi1, 'fire': f1}, index=drange)

	df.plot();
	plt.title("Daily Calls", fontsize=20)
	plt.xlabel('Date', fontsize=18)
	plt.xticks(fontsize=16)
	plt.ylabel("Number of Calls", fontsize=18)
	plt.yticks(fontsize=16)
	plt.savefig(join(output_dir, "daily_call_categories_during_covid.png"))
	plt.close()
	return df

def trendTest(output_dir, data): 
	"""
	Tests each of the call categories during a given time period for
	a monotonic trend by using the mann-kendall test. Results of this
	test are saved to a csv file.

	Inputs:
		- output_dir: String path to output directory
		- data: incident data of time period you want to graph
	"""
	call_categories = ['injuries_external', 'motor', 'health', 'fire', 'mental_illness', 'other']
	trend = []
	h = []
	p = []
	z =[]
	Tau = []
	s = []
	var_s = []
	slope = []

	for category in call_categories: 
	    category_data = data[[category]]
	    to, ho, po, zo, Tauo, so, var_so, slopeo = mk.original_test(category_data)
	    trend.append(to)
	    h.append(ho)
	    p.append(po)
	    z.append(zo)
	    Tau.append(Tauo)
	    s.append(so)
	    var_s.append(var_so)
	    slope.append(slopeo)
	    
	results = pd.DataFrame({'Call_Category':call_categories, 'Trend':trend, 'h':h, 'p':p,
	                       'z':z, 'Tau':Tau, 's':s, 'var_s':var_s, 'slope':slope})
	results.to_csv(join(output_dir, "trend_test_results.csv"), index=False)

call_category_map = {
    "FEAB": "health",
    "FEAV": "health",
    "FEBA": "health",
    "FECA": "health",
    "FECP": "health",
    "FEDI": "health",
    "FEHD": "health",
    "FEHV": "health",
    "FEHT": "health",
    "FEOB": "health",
    "FEPF": "health",
    "FEPV": "health",
    "FERE": "health",
    "FESE": "health",
    "FESI": "health",
    "FESV": "health",
    "FEST": "health",
    "FESY": "health",
    "FEUC": "health",
    "FEAR": "injuries_external",
    "FEVR": "injuries_external",
    "FEAS": "injuries_external",
    "FEBI": "injuries_external",
    "FEBL": "injuries_external",
    "FEBU": "injuries_external",
    "FECH": "injuries_external",
    "FEDR": "injuries_external",
    "FEEL": "injuries_external",
    "FEFA": "injuries_external",
    "FEFR": "injuries_external",
    "FEIJ": "injuries_external",
    "FEIN": "injuries_external",
    "FEPD": "injuries_external",
    "FEPO": "injuries_external",
    "FESG": "injuries_external",
    "FESH": "injuries_external",
    "FESW": "injuries_external",
    "FETA": "injuries_external",
    "FETE": "injuries_external",
    "FEMA": "motor",
    "FEMC": "motor",
    "FEAL": "mental_illness",
    "FEHG": "mental_illness",
    "FEOD": "mental_illness",
    "FEPS": "mental_illness",
    "FEUN": "other",
    "FEHZ": "other",
    "FEHU": "other",
    "FECK": "other",  # check patient
    "FEAM": "other",  # automatic alert
    "FEFD": "other",  # walk in
    "FESC": "other",  # HPD on scene
    "FEDA": "other",  # dead upon arrival
    "FEVJ": "other",  # fire stand by
    "FEAF": "other",  # assist the firefighter
    "FEET": "other",  # emergency transfer
    #### NEW MEDICAL CALLS ####
    "FEOF": "other",  # emergency assist the officer
    #### FIRE CALLS ####
    "FFDM": "fire",
    "FFGR": "fire",
    "FFTE": "fire",
    "FFAA": "fire",
    "FFOE": "fire",
    "FFMA": "fire",
    "FFHV": "fire",
    "FFLB": "fire",
    "FFMB": "fire",
    "FFEL": "fire",
    "FFUN": "fire",
    "FFSC": "fire",
    "FFSB": "fire",
    "FFHU": "fire",
    "FFGL": "fire",
    "FFCM": "fire",
    "FCON": "fire",
    "FMSC": "fire",
    "FFAL": "fire",
    "FFWR": "fire",
    "FFNO": "fire",
    "FFOR": "fire",
    "FFLV": "fire",
    "FFCH": "fire",
    "FFGN": "fire",
    "FFHR": "fire",
    "FFSP": "fire",
    "FFWD": "fire",
    "FHPD": "fire",
    "FFCL": "fire",
    "FFAF": "fire",
    "FFVJ": "fire",
    "FFTS": "fire",
    "FFCS": "fire",
    "FFTR": "fire",
    "FSCK": "fire",
    "FFSS": "fire",
    "FFHA": "fire",
    "FFBS": "fire",
    "FF31": "fire",
    "FF21": "fire",
    "FFAB": "fire",
    "FFES": "fire",
    "FFFW": "fire",
    "FFSH": "fire",
    "FPCK": "fire",
    "FFFD": "fire",
    "FF51": "fire",
    "FME": "fire",
    "FPDA": "fire",
    "FFPR": "fire",
    "FFSE": "fire",
    "FFAR": "fire",
    "FFPI": "fire",
    "FFAC": "fire",
    "FF41": "fire",
    "FFWA": "fire",
    "FFCO": "fire",
    "FTES": "other",
    "FSEV": "fire",
    "FPSE": "other",
    "FPSH": "other",
    "FPCP": "other",
    "FSTG": "fire",
    "FSHC": "fire",
    "NONE": "other",
    "FMP": "other",
    "F211": "other",
    "FMF": "other",
}
