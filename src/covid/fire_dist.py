from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

import src.covid.call_prob as call_prob
import src.covid.clustering as clustering
import src.covid.final_labels as final_labels
import src.covid.mapping as mapping

def run(output_dir, fd_data, fd_filepath): 
	"""
	Runs covid analysis for fire district level. 

	Inputs: 
		- output_dir: String path to output directory 
		- fd_data: Dataframe of indices and call prob aggregated at fire
			district level 
		- fd_filepath: String path to fire district geojson 
	"""
	covid_df = cluster(output_dir, fd_data)
	all_labelled = call_prob.assignCallDemandLabel(covid_df)
	final_df = final_labels.assign_labels(output_dir, all_labelled, filename="final_FD_category_counts.csv")
	mapping.makeSingleBGMap(output_dir, fd_filepath, 'feature.id', 'final-firedist-covid-clusters', final_df, 
		['index', 'final_cat_val'], 'Match Type', color="Spectral", bg=False)

def cluster(output_dir, fd_data):
	"""
	Runs clustering algorithm on fire district data. 

	Inputs: 
		- output_dir: String path to output directory 
		- fd_data: Dataframe of indices and call prob aggregated at fire
			district level 
	""" 
	fd_data = clustering.clustering(fd_data, 2)
	fd_data = clustering.nameClusters(fd_data)
	clustering.getClusterCenters(output_dir, fd_data, bg=False)
	return fd_data
