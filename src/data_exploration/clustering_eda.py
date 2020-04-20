import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

def swarmPlot(cluster_name = "cluster", factor_name, df, title="Swarmplot", 
	xlabel="Cluster Number", ylabel="Factor Name"): 
	"""
	Creates a swarmplot comparing the distribution of a single variable among clusters. 

	Input: 
	- cluster_name: string column name of the cluster labels 
	- factor_name: string column name of the factor to visualize 
	- df: dataframe of all the data 
	- title: string name of the plot 
	- xlabel: string name of the clusters 
	- ylable: string name of the factor being visualized 

	Output: A swarmplot comparing distribution of specified variable among clusters 
	"""
	plt.figure(figsize=(12,8))
	sns.swarmplot(x=cluster_name, y=factor_name, data=df)
	plt.title(title, fontsize=20)
	plt.ylabel(ylabel, fontsize=18)
	plt.yticks(fontsize=15)
	plt.xlabel(xlabel, fontsize=18)
	plt.xticks(fontsize=15)
	plt.show()

def plotIndexDistForCluster(cluster_data):
	"""
	Creates a 2x2 figure with the histogram of health, diversity, 
	poverty, and risk indices of the specified cluster. 

	Inputs: dataframe of all the datapoints in a given cluster 

	Output: a figure with histograms for each of the sub-indices 
	"""

    f, axs = plt.subplots(2,2)
    f.suptitle(catName)
    axs[0, 0].hist(data['Health_Affliction_Index'])
    axs[0, 0].set_title("Health Affliction Index Distribution")
    axs[0, 0].set_ylabel("Number of Block Groups")
    axs[0, 0].set_xlabel("Health Affliction Index Value")
    
    axs[0, 1].hist(data['Poverty_Index'])
    axs[0, 1].set_title("Poverty Index Distribution")
    axs[0, 1].set_ylabel("Number of Block Groups")
    axs[0, 1].set_xlabel("Poverty Index Value")
    
    axs[1, 0].hist(data['Diversity_Index'])
    axs[1, 0].set_title('Diversity Index Distribution')
    axs[1, 0].set_ylabel("Number of Block Groups")
    axs[1, 0].set_xlabel("Diversity Index Value")    

    axs[1, 1].hist(data['Risk_Index'])
    axs[1, 1].set_title('Risk Index')
    axs[1, 1].set_ylabel("Number of Block Groups")
    axs[1, 1].set_xlabel("Risk Index Value") 
