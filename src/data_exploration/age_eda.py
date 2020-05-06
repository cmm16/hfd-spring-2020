from os.path import join

import src.data_exploration.general_eda as general_eda


def run_age_eda(output_dir, train_df):
    """
	This function runs the age portion of EDA. 

	Inputs: 
		- output_dir: String path to output directory 
		- incidents_df: Dataframe of incidents that must include parsed time and call category
	"""
    avgs, portions_df, train_df = data_wrangling(output_dir, train_df)
    general_eda.plot_quartiles(output_dir, train_df, "avgAge", "Weighted Average Age")
    general_eda.plot_call_dist(
        output_dir,
        portions_df,
        "Age Quartiles",
        ["Youngest", "Middle Younger", "Middle Older", "Oldest"],
        "Age",
    )
    general_eda.chi_squared_test(output_dir, avgs, "Age")


def data_wrangling(output_dir, data):
    """
	This function prepares the data for age eda. First, the function adds 'avgAge',
	which is the weighted average age for the block group, to the dataframe passed in. 
	Then the function creates a table of proportions for each quartile. 

	Inputs: 
		- output_dir: String path to output directory
		- data: train_categories dataframe 

	Returns: 
		- dataframe of average number of calls per call category per quartile 
		- dataframe of call category proportion per quartile  
		- modified input dataframe with 'avgAge' column
	"""
    data["avgAge"] = (
        data["pctAge0004"] / 100 * 2
        + data["pctAge0017"] / 100 * 10.5
        + data["pctAdult1829"] / 100 * 23.5
        + data["pctAdult3044"] / 100 * 37
        + data["pctAdult4564"] / 100 * 54.5
        + data["pctAdult65p"] / 100 * 72.5
    )
    avgs, portions = general_eda.get_quantile_data("avgAge", data)
    avgs.to_csv(join(output_dir, "age_call_category_averages.csv"))
    return avgs, portions, data
