import pandas as pd
from os import path
from os import getcwd


def format_inc_cad(file):
    """
    This code should be added to the cad_wrangling.py file
    As is, we take in the one of the outputs of cad_wrangling.py, which is a file called
    inc_cad_clean. We then merge it with the call types xlsx file and reformat to be usable for
    data exploration.

    :param file: "CAD Call Types - ImageTrend values.xlsx"
    :return: clean data frame of inc_cad
    """

    inc_df = pd.read_csv(file)  # The file right now is inc_cad_clean.csv
    inc_df = inc_df.rename(
        columns={'0': "Incident_ID",
                 '1': "Call_Type",
                 '2': 'Address',
                 '3': "City_ID",
                 '4': 'Longitude',
                 '5': 'Latitude'}
    )

    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    call_data = path.join(data_dir, "CAD Call Types - ImageTrend values.xlsx")

    call_df = pd.read_excel(
        call_data
    )  # This is an excel file that has the call type codes and descriptions

    call_df = call_df.rename(
        columns={'TYPE': "Call_Type",
                 'DESCRIPTION': 'Description',
                 "DEFAULT PRIOITY": "Default_Priority"}
    )  # Rename columns for Merging and for Standard Naming Procedures

    formatted_inc_df = pd.merge(inc_df,
                                call_df,
                                on='Call_Type')  # Merge on Key Call_Type

    return formatted_inc_df
