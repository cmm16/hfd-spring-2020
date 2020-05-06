from os.path import join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# Global variable for defining call category columns
call_cols = ["health", "injuries_external", "mental_illness", "motor", "fire", "other"]

#########################################################################
# 					WRANGLING & TEST FUNCTIONS					 		#
#########################################################################


def chi_squared_test(output_dir, counts_df, type):
    """
	This function calculates a chi-squared test for a given 
	subgroups of a demographic factor. 

	Inputs: 
		- output_dir: String path to output directory
		- counts_df: dataframe where each row is a category, and 
			columns are call category average
		- type: String describing demographic factor 
	"""
    single_list = []
    for row in range(counts_df.shape[0]):
        single_list.append(counts_df.iloc[row][call_cols])
    single = np.array(single_list)
    chi2_stat, p_val, dof, ex = stats.chi2_contingency(single)
    f = open(output_dir + "/" + type + "_chi_squared_test.txt", "a")
    f.write("===Chi2 Stat===" + "\n")
    f.write(str(chi2_stat) + "\n")
    f.write("===Degrees of Freedom===" + "\n")
    f.write(str(dof) + "\n")
    f.write("===P-Value===" + "\n")
    f.write(str(p_val) + "\n")
    f.write("===Contingency Table===" + "\n")
    f.write(str(ex) + "\n")
    f.close()


def calculate_total_calls(data):
    """
	This function calculates total calls for a given input dataframe, and returns 
	the sum of the calls and calls per cap as new columns. 
	"""
    data["total_calls"] = 0
    for call in call_cols:
        data["total_calls"] += data[call]
    # Standardize per capita
    data["total_calls_per_cap"] = data["total_calls"] / data["TotalPop"]
    return data


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
    data = calculate_total_calls(data)
    # Calculate quantiles
    q25 = data[column].quantile(0.25)
    q50 = data[column].quantile(0.5)
    q75 = data[column].quantile(0.75)
    # Create subset of each quartile
    q1df = data[data[column] <= q25]
    q2df = data[(data[column] > q25) & (data[column] <= q50)]
    q3df = data[(data[column] > q50) & (data[column] <= q75)]
    q4df = data[data[column] > q75]
    # Get average number of calls of each type
    q1_mean = q1df[call_cols + ["total_calls", "total_calls_per_cap"]].mean()
    q2_mean = q2df[call_cols + ["total_calls", "total_calls_per_cap"]].mean()
    q3_mean = q3df[call_cols + ["total_calls", "total_calls_per_cap"]].mean()
    q4_mean = q4df[call_cols + ["total_calls", "total_calls_per_cap"]].mean()
    # Make dataframe of averages
    avgs = pd.DataFrame([q1_mean, q2_mean, q3_mean, q4_mean])
    # Convert to proportions
    portions = avgs[call_cols].apply(lambda row: row / row.sum(), axis=1)
    portions["quartile"] = ""
    portions.at[0, "quartile"] = "Lowest"
    portions.at[1, "quartile"] = "Middle-Lowest"
    portions.at[2, "quartile"] = "Middle-Upper"
    portions.at[3, "quartile"] = "Highest"
    return avgs, portions


#########################################################################
# 						PLOTTING FUNCTIONS						 		#
#########################################################################


def plot_volume_chart(output_dir, df, title, xaxis_label, xticks, xtick_labels):
    """
	Creates a bar chart of average calls per block group. 

	Inputs: 
		- output_dir: String path to output directory
		- df: dataframe where each row is a category, and there is a 
			"total_calls" column with the average call 
		- title: string title of graph 
		- xaxis_label: string to label x-axis 
		- xticks: array of number of ticks on x-axis 
		- xtick_labels: array of strings for each x-tick label 
	"""
    plt.figure(figsize=(10, 10))
    df.total_calls_per_cap.plot(
        kind="bar", color=["coral", "red", "darkorange", "firebrick"]
    )
    plt.title(title, fontsize=20)
    plt.ylabel("Average Call Volume", fontsize=18)
    plt.yticks(fontsize=15)
    plt.xlabel(xaxis_label, fontsize=18)
    plt.xticks(ticks=xticks, labels=xtick_labels, fontsize=15, rotation=0)
    plt.savefig(join(output_dir, title + ".png"))


def plot_donut_chart(output_dir, values, labels, description):
    """
	TODO
	"""
    plt.figure(figsize=(10, 10))

    # Create a circle for the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color="white")

    # Give color names
    plt.pie(
        values,
        labels=labels,
        colors=["darkorange", "red", "coral", "firebrick", "gold"],
    )  # fire themed
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.savefig(join(output_dir, description + "_donut_chart.png"))


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
    plt.figure(figsize=(12, 8))
    data[column].hist(bins=100)
    # Get quartiles and add as line
    q25 = data[column].quantile(0.25)
    q50 = data[column].quantile(0.5)
    q75 = data[column].quantile(0.75)
    plt.plot([q25, q25], [0, 500], linewidth=3)
    plt.plot([q50, q50], [0, 500], linewidth=3)
    plt.plot([q75, q75], [0, 500], linewidth=3)
    plt.ylim(0, 55)

    # Plot attributes
    plt.title(column_name + " Distribution", fontsize=20)
    plt.ylabel("Number of Block Groups", fontsize=18)
    plt.yticks(fontsize=15)
    plt.xlabel(column_name, fontsize=18)
    plt.xticks(fontsize=15)
    plt.legend(["25th Quartile", "50th Quartile", "75th Quartile"])
    plt.savefig(join(output_dir, column_name + "_quartiles.png"))


def plot_call_dist(output_dir, portions_df, xlabel, labels, factor):
    """
	This function creates a stacked bar chart of the call proportions 
	for each quantile.  

	Inputs: 
		- output_dir: String path to output directory
		- portions_df: dataframe where each row is a category, and 
			columns are call category proportions
		- xlabel: String describing name of x axis 
		- labels: array of strings to rename xticks
		- factor: String describing demographic factor plot is about 
	"""
    callLabels = [
        "Health (internal)",
        "External Injuries",
        "Mental Illness",
        "Motor",
        "Fire",
        "Other",
    ]
    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(111)
    portions_df.plot(
        ax=ax,
        kind="bar",
        stacked=True,
        rot=0,
        color=["coral", "red", "yellow", "darkorange", "firebrick", "gold"],
    )
    plt.title("Call Distribution", fontsize=20)
    plt.ylabel("Proportion of Calls", fontsize=18)
    plt.yticks(fontsize=15)
    plt.xlabel(xlabel, fontsize=18)
    plt.legend(prop={"size": 20}, labels=callLabels)
    plt.xticks(ticks=[0, 1, 2, 3], labels=labels, fontsize=15)
    plt.savefig(join(output_dir, factor + "_call_dist.png"))
