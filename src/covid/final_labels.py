from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

import src.covid.mapping as mapping

def run(output_dir, df, bg_filepath): 
	"""
	Runs final labelling aggregations for covid-19 risk assessment.

    Inputs:
        - output_dir: String path to output directory
        - df: Dataframe with covid-19 risk level and call demand level per block group
        - bg_filepath: String path to block group geojson file
	"""
	labelled = assign_labels(output_dir, df)
	mapping.makeSingleBGMap(output_dir, bg_filepath, 'feature.properties.Name', 'final-covid-clusters', labelled, 
		['Block_Group', 'final_cat_val'], 'Match Type', color="Spectral")

def assign_labels(output_dir, data, filename="final_category_counts.csv"): 
	"""
	Assigns labels to block groups based on both covid-19 risk level and call demand level.

    Inputs:
        - output_dir: String path to output directory
        - df: Dataframe with covid-19 risk level and call demand level per block group
        - filename: String specifying where to save count results to

    Returns: modified input dataframe with final labels in new column
    """
	# match or mismatch?
	data.loc[(data.cluster_name == "high") & (data.prob_call_level == "high"), 'final_category_type'] = "match"
	data.loc[(data.cluster_name == "low") & (data.prob_call_level == "low"), 'final_category_type'] = "match"
	data.loc[(data.cluster_name == "high") & (data.prob_call_level == "low"), 'final_category_type'] = "mismatch"
	data.loc[(data.cluster_name == "low") & (data.prob_call_level == "high"), 'final_category_type'] = "mismatch"
	
	# what levels?
	data.loc[(data.cluster_name == "high") & (data.prob_call_level == "high"), 'final_category'] = "match-high"
	data.loc[(data.cluster_name == "low") & (data.prob_call_level == "low"), 'final_category'] = "match-low"
	data.loc[(data.cluster_name == "high") & (data.prob_call_level == "low"), 'final_category'] = "mismatch-high-low"
	data.loc[(data.cluster_name == "low") & (data.prob_call_level == "high"), 'final_category'] = "mismatch-low-high"

	# assign numerical value
	data.loc[(data.final_category == "match-high"), 'final_cat_val'] = 1
	data.loc[(data.final_category == "match-low"), 'final_cat_val'] = 2
	data.loc[(data.final_category == "mismatch-high-low"), 'final_cat_val'] = 0
	data.loc[(data.final_category == "mismatch-low-high"), 'final_cat_val'] = 3

	counts = pd.DataFrame(data.groupby(['cluster_name', 'prob_call_level']).Poverty_Index.count().reset_index())

	counts.to_csv(join(output_dir, filename))

	return data 