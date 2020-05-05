from os.path import join, dirname
import pandas as pd
from os import getcwd, mkdir

from time_eda import run_time_eda
from race_eda import run_race_eda
from age_eda import run_age_eda
from income_eda import run_income_eda
from language_eda import run_language_eda

# incidents_df = pd.read_csv("test/imagetrend_incidents.csv")
# train_df = pd.read_csv("test/final_train_categories.csv")

def main(output_dir):
    mkdir(output_dir)

    run_time_eda(output_dir, incidents_df) 
    run_race_eda(output_dir, train_df)
    run_age_eda(output_dir, train_df)
    run_income_eda(output_dir, train_df)
    run_language_eda(output_dir, train_df)

if __name__ == '__main__':
    main(join(dirname(dirname(getcwd())), "eda_output"))