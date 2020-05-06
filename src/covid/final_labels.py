from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

import src.covid.mapping as mapping

def run(output_dir, df, bg_filepath): 
	labelled = assign_labels(output_dir, df)
	mapping.makeSingleBGMap(output_dir, bg_filepath, 'feature.properties.Name', 'final-covid-clusters', labelled, 
		['Block_Group', 'final_cat_val'], 'Match Type', color="Spectral")

def assign_labels(output_dir, data, filename="final_category_counts.csv"): 
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