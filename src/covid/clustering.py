from os.path import join

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

import src.covid.mapping as mapping

indices = ['Health_Affliction_Index', 'Poverty_Index', 'Diversity_Index']

def run(output_dir, incidents, bg_filepath):

	# k was found using the NBClust package in R 
	# for our data, we found that the 2 clusters was the most optimal 
	clustered_df = clustering(incidents, k=2)
	clustered_df = nameClusters(clustered_df)
	plotPoints(output_dir, clustered_df, False)
	plotPoints(output_dir, clustered_df, True)
	getClusterCenters(output_dir, clustered_df)
	plotHistograms(output_dir, clustered_df)
	plotCallDist(output_dir, clustered_df, [0,1], ['Low', 'High'])

	map_df = clustered_df[['Block_Group', 'cluster']]
	map_df['cluster_inv'] = abs(1 - map_df['cluster'])
	mapping.makeSingleBGMap(output_dir, bg_filepath, 'feature.properties.Name', 'Risk-clusters', map_df, 
		['Block_Group', 'cluster_inv'], 'Risk Level')
	return clustered_df

def clustering(df, k): 
	df = df.fillna(df.median(0))
	X = df[indices]
	kmeans = KMeans(init='k-means++', n_clusters=k, 
	                n_init=10, random_state=911).fit(X)
	centers = kmeans.cluster_centers_
	labels = kmeans.predict(X)
	df['cluster'] = labels
	return df 

def nameClusters(df): 
	df.loc[df.cluster == 0, 'cluster_name'] = "low"
	df.loc[df.cluster == 1, 'cluster_name'] = "high"
	return df 

def getClusterCenters(output_dir, df, bg=True): 
	# Create subset of each cluster 
	c0 = df[df['cluster'] == 0]
	c1 = df[df['cluster'] == 1]
	if bg: 
		indices = ['Health_Affliction_Index','Poverty_Index','Diversity_Index','Risk_Index']
	else: 
		indices = ['Health_Affliction_Index','Poverty_Index','Diversity_Index']	
	c0_stats = c0[indices].mean()
	c1_stats = c1[indices].mean()

	avg = pd.DataFrame([c0_stats,c1_stats])
	avg.to_csv(join(output_dir, "cluster-averages.csv"))

def plotPoints(output_dir, df, color_point=False): 
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
	for index in indices: 
		df.groupby(['cluster'])[index].hist(alpha=0.55);
		plt.legend(['Low','High'])
		plt.xlabel(index)
		plt.ylabel('Number of Block Groups')
		plt.title("Block Group"+index+" Distribution")
		plt.savefig(join(output_dir, index+"_cluster_distribution.png"))
		plt.close()

def plotCallDist(output_dir, df, xticks, xlabels): 
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
	plt.xticks(ticks=xticks,labels=xlabels, fontsize=15)
	plt.savefig(join(output_dir, "cluster_call_distribution.png"))



