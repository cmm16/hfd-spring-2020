from os.path import join

import pandas as pd

import src.data_exploration.general_eda as general_eda


def run_language_eda(output_dir, train_df):
    """
	This function runs the language portion of EDA. 

	Input: 
		- output_dir: String path to output directory 
		- train_df: Dataframe of census and call counts per block group 
	"""
    lang = data_wrangling(train_df)
    lang.to_csv(join(output_dir, "lang_call_category_averages.csv"))
    general_eda.chi_squared_test(output_dir, lang, "Language")
    general_eda.plot_volume_chart(
        output_dir,
        lang,
        "Average Calls per Primary Language",
        "Household Language",
        [0, 1],
        ["English", "Not English"],
    )


def data_wrangling(df):
    """
	This function prepares the data for volume bar graph. 
	
	Input: 
		- df: Dataframe of census and call counts per block group 
	"""
    df = general_eda.calculate_total_calls(df)
    # Subset english and non-english speaking block groups
    engl_blocks = df[df["pctLangEngl"] >= 50]
    notengl_blocks = df[df["pctLangNEngl"] >= 50]
    # Calculate average of each type
    columns = [
        "health",
        "injuries_external",
        "mental_illness",
        "motor",
        "fire",
        "other",
        "total_calls",
        "total_calls_per_cap",
    ]
    eng_df = engl_blocks[columns].mean()
    not_eng_df = notengl_blocks[columns].mean()
    lang = pd.DataFrame([eng_df, not_eng_df])
    return lang
