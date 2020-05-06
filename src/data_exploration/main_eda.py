import os
import shutil
from os import getcwd, mkdir
from os.path import join, dirname

import pandas as pd

from src.data_exploration.age_eda import run_age_eda
from src.data_exploration.airport_eda import run_airports_eda
from src.data_exploration.income_eda import run_income_eda
from src.data_exploration.language_eda import run_language_eda
from src.data_exploration.race_eda import run_race_eda
from src.data_exploration.time_eda import run_time_eda


def main(data_dir):
    output_dir = join(dirname(data_dir), "eda_output")

    if not os.path.exists(output_dir):
        mkdir(output_dir)
    else:
        shutil.rmtree(output_dir)  # Removes all the subdirectories!
        mkdir(output_dir)

    incidents_df = pd.read_csv(join(data_dir, "inc_cad_clean_with_loc.csv"))
    train_df = pd.read_csv(join(data_dir, "final_train_categories.csv"))
    with_airports_df = pd.read_csv(join(data_dir, "with_airports_for_eda.csv"))

    run_airports_eda(output_dir, with_airports_df)
    run_time_eda(output_dir, incidents_df)
    run_race_eda(output_dir, train_df)
    run_age_eda(output_dir, train_df)
    run_income_eda(output_dir, train_df)
    run_language_eda(output_dir, train_df)

    ## NEEDS MODEL OUTPUT SO PROB MOVE TO MODELLING SECTION ##
    run_map_maker(output_dir, model_output, bg_filepath, fd_filepath)

if __name__ == '__main__':
    main(join(dirname(dirname(getcwd())), "eda_output"))