from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

def run(output_dir, df): 
	df = calculate_probability(df)
	plotCallDemandDistribution(output_dir, df)
	labelled = assignCallDemandLabel(df)
	return labelled 

def calculate_probability(data):
	data['total_calls'] = data['fire']+data['health']+data['injuries_external']+data['mental_illness']+data['motor']+data['other']
	total_calls =  data['total_calls'].sum()
	data['prob_call'] = (data['total_calls']/total_calls)
	return data

def plotCallDemandDistribution(output_dir, df): 
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
	avg = data.prob_call.mean()
	data.loc[data.prob_call >= avg, 'prob_call_level'] = "high"
	data.loc[data.prob_call < avg, 'prob_call_level'] = "low"
	return data 

