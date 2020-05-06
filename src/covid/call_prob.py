from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

def run(output_dir, df): 
	"""
	Runs entire call probability process. 

    Inputs: 
        - output_dir: String path to output directory 
        - df: Dataframe with call counts per block group 

    Returns: dataframe with call demand string label assigned. 
	"""
	df = calculate_probability(df)
	plotCallDemandDistribution(output_dir, df)
	labelled = assignCallDemandLabel(df)
	return labelled 

def calculate_probability(data):
	"""
	Calculates call probability for each block group and adds as a new column 
	to input dataframe. 

	Inputs: 
		- data: dataframe of call counts per block group 

	Returns: modified input dataframe with call probability column 
	"""
	data['total_calls'] = data['fire']+data['health']+data['injuries_external']+data['mental_illness']+data['motor']+data['other']
	total_calls =  data['total_calls'].sum()
	data['prob_call'] = (data['total_calls']/total_calls)
	return data

def plotCallDemandDistribution(output_dir, df): 
	"""
	Plots distribution of call demands with a line at the mean. 

    Inputs: 
        - output_dir: String path to output directory 
        - df: Dataframe with call probability calculated 
	"""
	plt.figure(figsize=(10,6))
	df.prob_call.hist(bins=50)
	avg = df.prob_call.mean()
	plt.plot([avg, avg], [0, 500], linewidth=5)
	plt.ylim(0, 400)
	plt.title("Probability of Calling Distribution", fontsize=20)
	plt.xlabel("Probability of Calling", fontsize=18)
	plt.xticks(fontsize=15)
	plt.ylabel("Number of Block Groups", fontsize=18)
	plt.yticks(fontsize=15)
	plt.savefig(join(output_dir, "call_demand_dist.png"))

def assignCallDemandLabel(data): 
	"""
	Splits block groups into high vs. low call demand and assigns 
	string label in new column. 

	Inputs: 
		- df: Dataframe with call probability calculated 

	Returns: modified input dataframe with string label of call demand level 
	"""
	avg = data.prob_call.mean()
	data.loc[data.prob_call >= avg, 'prob_call_level'] = "high"
	data.loc[data.prob_call < avg, 'prob_call_level'] = "low"
	return data 

