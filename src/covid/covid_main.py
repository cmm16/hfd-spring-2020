import shutil
from os import getcwd, mkdir
from os.path import join, dirname, exists

import pandas as pd

import src.covid.call_prob as call_prob
import src.covid.clustering as clustering
import src.covid.final_labels as final_labels
import src.covid.time_eda as time_eda
import src.covid.fire_dist as fire_dist


def main(data_dir):
    output_dir = join(dirname(data_dir), "covid_output")

    if not exists(output_dir):
        mkdir(output_dir)
    else:
        shutil.rmtree(output_dir)  # Removes all the subdirectories!
        mkdir(output_dir)

    incidents = pd.read_csv(join(data_dir, "inc_cad_clean_with_loc.csv"))
    data = pd.read_csv(join(data_dir, "covid_indices.csv"))
    fd_data = pd.read_csv(join(data_dir, "firedist_covid.csv"))
    bg_filepath = join(
        join(join(data_dir, "Uploaded_Shapefiles"), "CensusBlock_2010"),
        "Census_FIP12_within_Fire_Dis.geojson",
    )
    fd_filepath = join(
        join(join(data_dir, "Uploaded_Shapefiles"), "Fire_Districts"),
        "fire_districts.geojson",
    )
    ### BLOCK GROUP FUNCTIONS ### 
    time_eda.run(output_dir, incidents)
    clustered_df = clustering.run(output_dir, data, bg_filepath)
    all_labelled = call_prob.run(output_dir, clustered_df)
    final_labels.run(output_dir, all_labelled, bg_filepath)
    ### FIRE DISTRICT FUNCTIONS ### 
    fire_dist.run(output_dir, fd_data, fd_filepath)


if __name__ == "__main__":
    main(join(dirname(dirname(getcwd())), "Data"))
