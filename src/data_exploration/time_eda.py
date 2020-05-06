from os.path import join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


def run_time_eda(output_dir, incidents_df):
    """
	This function runs the time portion of EDA. 

	Input: 
		- output_dir: String path to data directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	"""
    timedf = data_wrangle(incidents_df)
    plot_raw_data(output_dir, timedf)
    plot_decomposition(output_dir, timedf)
    plot_yearly_dist(output_dir, incidents_df)


def data_wrangle(df, start_date="2013-01", level="Day"):
    """
	This function prepares the data for analysis by counting the number of 
	incidents per day. The counted data is then unstacked and flattened into a 
	dataframe with a single column. 

	Input: 
		- df: Dataframe with columns "Event_Number", Year", "Month", "Date" (optional)
		- start_date: String indicating first day of data in "YYYY-MM" format

	Returns:
		- a single column data frame of the data 
	"""
    groupBy = df.groupby(["Year", "Month", "Date"]).count()["Event_Number"].unstack(0)
    all_data = groupBy.values.flatten(order="F")
    flat_data = all_data[~np.isnan(all_data)]

    N = len(flat_data)
    drange = pd.date_range(start_date, periods=N)
    timedf = pd.DataFrame(flat_data, index=drange)

    return timedf


def plot_raw_data(
    output_dir, timedf, title="Daily Number of Calls from 1/1/2013 - 4/12/2020"
):
    """
	This function creates a time series plot and saves it to specified output directory. 

	Input: 
		- output_dir: String of path to eda outputs
		- timedf: single column data frame of daily call counts 
		- title: String title of plot
	"""
    timedf.plot(figsize=(15, 10))
    plt.title(title, fontsize=20)
    plt.xlabel("Date", fontsize=18)
    plt.xticks(fontsize=16)
    plt.ylabel("Number of Calls", fontsize=18)
    plt.yticks(fontsize=16)
    plt.savefig(join(output_dir, "timeseries.png"))


def plot_decomposition(output_dir, timedf):
    """
	This function creates a seasonal decomposition plot and saves it to 
	specified output directory. 

	Input: 
		- output_dir: String of path to eda outputs
		- timedf: single column data frame of daily call counts 
	"""
    result = seasonal_decompose(timedf, model="additive", freq=365)
    plt.rcParams["figure.figsize"] = [15, 10]
    result.plot()
    plt.xlabel("Date")
    plt.savefig(join(output_dir, "timeseries_decomposition.png"))

def plot_yearly_dist(output_dir, incidents_df): 
    """
    Creates stacked bar chart of call distribution for each year.

    Input:
    - output_dir: String path to data directory
    - incidents_df: Dataframe of incidents that must include parsed time and call category
    """
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(111)
    incidents_df["Subcall_Code"] = incidents_df["Event_Type"].str[:4]
    incidents_df["Call_Category"] = incidents_df["Subcall_Code"].apply(
    lambda x: call_category_map[x])
    years = incidents_df.groupby(["Year", "Call_Category"]).Event_Number.count().unstack(1)
    callsPercent = years.apply(lambda row: row/row.sum(), axis=1)
    callsPercent.plot(ax=ax,kind='bar', stacked=True, rot=0, color=['coral', 'red', 'yellow', 'darkorange', 'firebrick', 'gold'])
    mylabels = ["Health (internal)", "External Injuries", "Mental Illness", "Motor", 'Fire', 'Other']
    plt.title("Yearly Call Distribution", fontsize=20)
    plt.ylabel("Portion of Calls", fontsize=18)
    plt.yticks(fontsize=15)
    plt.xlabel("Year", fontsize=18)
    plt.xticks(fontsize=15)
    plt.legend(labels = mylabels)
    plt.savefig(join(output_dir, "yearly_call_distribution.png"))


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
