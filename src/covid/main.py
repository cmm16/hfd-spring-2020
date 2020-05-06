from os import getcwd, mkdir
from os.path import join, dirname

import pandas as pd

import src.covid.call_prob as call_prob
import src.covid.clustering as clustering
import src.covid.final_labels as final_labels
import src.covid.time_eda as time_eda

### Sample file paths ###
incidents = pd.read_csv("test/imagetrend_incidents.csv")
data = pd.read_csv("test/covid_indices.csv")
bg_filepath = "test/Census_FIP12_within_Fire_Dis.geojson"


def main(output_dir):
    mkdir(output_dir)

    time_eda.run(output_dir, incidents)
    clustered_df = clustering.run(output_dir, data, bg_filepath)
    all_labelled = call_prob.run(output_dir, clustered_df)
    final_labels.run(output_dir, all_labelled, bg_filepath)


if __name__ == "__main__":
    main(join(dirname(dirname(getcwd())), "covid_output"))
