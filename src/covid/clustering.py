from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import mapping 
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.lines as mlines

indices = ['Health_Affliction_Index', 'Poverty_Index', 'Diversity_Index']

def run(output_dir, df, bg_filepath):
	"""
	Runs entire clustering portion including creating visualizations. 

	Inputs: 
		- output_dir: String path to output directory 
		- df: Dataframe of base indices for every block group 
		- bg_filepath: String file path to block group geojson 
	
	Returns: dataframe with cluster numeric and string label. 
	"""

	# k was found using the NBClust package in R 
	# for our data, we found that the 2 clusters was the most optimal 
	clustered_df = clustering(df, k=2)
	clustered_df = nameClusters(clustered_df)
	# Create 3D Plots
	plotPoints(output_dir, clustered_df, False)
	plotPoints(output_dir, clustered_df, True)
	# Save cluster centers to csv
	getClusterCenters(output_dir, clustered_df)
	# Create histograms of each index 
	plotHistograms(output_dir, clustered_df)
	# Plot call distribution per cluster 
	plotCallDist(output_dir, clustered_df, ['Low', 'High'])

	# Create map of clusters
	map_df = clustered_df[['Block_Group', 'cluster']]
	map_df['cluster_inv'] = abs(1 - map_df['cluster'])
	mapping.makeSingleBGMap(output_dir, bg_filepath, 'feature.properties.Name', 'Risk-clusters', map_df, 
		['Block_Group', 'cluster_inv'], 'Risk Level')
	return clustered_df

def clustering(df, k): 
	"""
	This function uses k-means clustering to cluster the data. 

	Inputs: 
		- df: Dataframe of base indices for every block group 
		- k: number of clusters to make 

	Returns: modified input dataframe with column called 'cluster' and 
		numeric label of the cluster the observation is in 
	"""
	df = df.fillna(df.median(0))
	X = df[indices]
	kmeans = KMeans(init='k-means++', n_clusters=k, 
	                n_init=10, random_state=911).fit(X)
	centers = kmeans.cluster_centers_
	labels = kmeans.predict(X)
	df['cluster'] = labels
	return df 

def nameClusters(df): 
	"""
	This function assigns a string name to each cluster. 

	Inputs: 
		- df: Dataframe of base indices for every block group 
		- k: number of clusters to make 

	Returns: modified input dataframe with column called 'cluster_name' and 
		string name of the associated cluster the observation is in 
	"""
	df.loc[df.cluster == 0, 'cluster_name'] = "low"
	df.loc[df.cluster == 1, 'cluster_name'] = "high"
	return df 

def getClusterCenters(output_dir, df, bg=True): 
	"""
	This function gets the centers of each cluster and saves to a csv file. 

	Inputs: 
		- output_dir: String path to output directory 
		- df: Dataframe of base indices for every block group 
		- bg: True if analyzing at the block group level, otherwise false
			(e.g. analyzing at fire district level)
	"""
	# Create subset of each cluster 
	c0 = df[df['cluster'] == 0]
	c1 = df[df['cluster'] == 1]
	if bg: 
		indices = ['Health_Affliction_Index','Poverty_Index','Diversity_Index','Risk_Index']
	else: 
		indices = ['Health_Affliction_Index','Poverty_Index','Diversity_Index']	
	# Create dataframe of averages
	c0_stats = c0[indices].mean()
	c1_stats = c1[indices].mean()
	avg = pd.DataFrame([c0_stats,c1_stats])
	avg.to_csv(join(output_dir, "cluster-averages.csv"))

def plotPoints(output_dir, df, color_point=False):
	"""
	This function plots the block groups along the 3 base indices dimensions. 

	Inputs: 
		- output_dir: String path to output directory 
		- df: Dataframe of base indices for every block group 
		- color_point: false unless specified that the plot should be in color 
	""" 
	fig = plt.figure(figsize=(10, 8))
	ax = plt.axes(projection='3d')
	zdata = df['Health_Affliction_Index']
	ydata = df['Poverty_Index']
	xdata = df['Diversity_Index']
	if color_point: 
		color = df["cluster"]
		ax.scatter3D(xdata, ydata, zdata, edgecolors='black', s=40, c=color, cmap="coolwarm")
		blue_dot = mlines.Line2D([], [], color='blue', marker='.', linestyle='None', markersize=10, label='Blue point')
		red_dot = mlines.Line2D([], [], color='red', marker='.', linestyle='None', markersize=10, label='Red point')
		ax.legend([red_dot, blue_dot], ["High Risk", "Low Risk"], loc = 'lower right')
	else: 
		ax.scatter3D(xdata, ydata, zdata, edgecolors='black', s=40, c='1')
	ax.set_zlabel("Health_Affliction_Index")
	ax.set_ylabel("Poverty_Index")
	ax.set_xlabel("Diversity_Index")
	ax.set_title("Block Groups", fontsize=25, y=1.01, x= .50)
	ax.plot([0.42], [0.56], [0.91], color='red')
	ax.plot([0.36], [0.18], [0.36], color='blue')
	if color_point: 
		plt.savefig(join(output_dir, "3d-blockgroups-colored.png"))
	else: 
		plt.savefig(join(output_dir, "3d-blockgroups.png"))
	plt.close()

def plotHistograms(output_dir, df):
	"""
	This function creates a layered histogram of each base index 
	for each of the clusters. 

	Inputs: 
		- output_dir: String path to output directory 
		- df: Dataframe of base indices for every block group with cluster label  
	"""
	for index in indices: 
		df.groupby(['cluster'])[index].hist(alpha=0.55);
		plt.legend(['Low','High'])
		plt.xlabel(index)
		plt.ylabel('Number of Block Groups')
		plt.title("Block Group"+index+" Distribution")
		plt.savefig(join(output_dir, index+"_cluster_distribution.png"))
		plt.close()

def plotCallDist(output_dir, df, xlabels): 
	"""
	Create stacked bar chart of average call distribution per cluster. 

	Inputs: 
		- output_dir: String path to output directory 
		- df: Dataframe of base indices for every block group with cluster label 
		- xlabels: array of strings to label the x-axis 
	"""
	call_cols = ['health','injuries_external','mental_illness', 'motor', 'fire', 'other']
	c0 = df[df['cluster'] == 0]
	c1 = df[df['cluster'] == 1]
	c0_stats = c0[call_cols].mean()
	c1_stats = c1[call_cols].mean()
	avg = pd.DataFrame([c0_stats,c1_stats])
	callsPercent = avg.apply(lambda row: row/row.sum(), axis=1)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	callsPercent.plot(ax=ax,kind='bar', stacked=True, rot=0, color=['coral', 'red', 'yellow', 'darkorange', 'firebrick', 'gold'])
	plt.title("Cluster Call Distribution", fontsize=20)
	plt.ylabel("Portion of Calls", fontsize=18)
	plt.yticks(fontsize=15)
	plt.xlabel("Cluster Risk Type", fontsize=18)
	plt.xticks(ticks=[0,1],labels=xlabels, fontsize=15)
	plt.savefig(join(output_dir, "cluster_call_distribution.png"))



