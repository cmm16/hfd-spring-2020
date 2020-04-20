import pandas as pd 
from sklearn.cluster import KMeans

def prep(df): 
	"""
	Function that prepares the data for k-means algorithm by making sure 
	there are no NA values. 

	Input: dataframe df of data 
	Output: modified dataframe with no NA values 
	"""
	if (df.isna().values.any()): 
		df = df.fillna(df.median(0))
	return df 

def kMeansCluster(k, X): 
	"""
	Function that runs k-means algorithm and clusters data set. 

	Input: 
	- k: the number of clusters 
	- X: dataframe of attributes to cluster 

	Output: an array of the cluster labels for each entry
	in the data frame 
	"""
	kmeans = KMeans(init='k-means++', n_clusters=k, 
                n_init=10, random_state=911).fit(X)
	labels = kmeans.predict(X)
	return labels 

def clusterData(df, k, columns, result_name="Cluster_Number"): 
	"""
	Function that takes a dataframe and runs k-means clustering
	on specified columns and appends results as new column. 

	Input: 
	- df: dataframe of data 
	- k: number of clusters 
	- columns: column names to cluster the data on 
	- result_name: name of column for results 

	Returns: modified dataframe with additional result column that
	contains the cluster number for that entry. 
	"""	
	labels = kMeansCluster(k, df[columns])
	df[result_name] = labels 
	return df 

def interpClusters(df, clusterDict, cluster_column_name, interp_column_name = "Cluster_Name"):
	"""
	Function that assigns a cluster number an interpretable value. 
	For example: cluster 0 = "high risk" cluster 

	Input: 
	- df: dataframe of data with labelled clusters 
	- clusterDict: mapping of cluster number to interpretable string label 
	- cluster_column_name: string name of the cluster column 
	- interp_column_name: string name of the column to put interpretable cluster result 

	Returns: modified dataframe with new column of interpretable results 
	"""
	for key in clusterDict.keys(): 
		df.loc[df.cluster_column_name == key, interp_column_name] = clusterDict[key]
	return df 

def averages(k, columns, df, cluster_column_name):
	"""
	Creates a dataframe of the averages of each cluster. 

	Inputs: 
	- k: number of clusters 
	- columns: list of string column names of factors to take average of 
	- df: dataframe of all the data 
	- cluster_column_name: string name of the column with cluster numbers 

	Returns: dataframe with average specified column values for clusters 
	"""
	stats = []
	for cluster_num in range(k): 
		temp = df[df.cluster_column_name == cluster_num]
		stats.append(temp_stats.mean())
	return pd.DataFrame(stats)


