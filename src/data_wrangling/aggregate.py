import pandas as pd
from os import path
from os import getcwd


def compute_bg_column(df):
    df["Block_Group"] = df.location.astype(str).str[:12].astype(float)
    return df


def aggregate_call_type(df, groupby_columns):
    """
    This function will group a dataframe by specified columns and count the number of entries in the specified groups.

    Inputs:
        - df: the dataframe to perform calculations on
        - groupby_columns: a list of the columns to group by
    Returns: a dataframe with the counts per group
    """
    counts = df.groupby(groupby_columns).size()
    return counts.unstack(fill_value = 0)


def aggregate():
    df = pd.read_csv(path.join(path.dirname(path.dirname(getcwd())), "data/inc_cad_clean_with_loc.csv"))
    df = compute_bg_column(df)
    aggregate_df = aggregate_call_type(df, ["Block_Group", "Call_Type"])
    aggregate_df.to_csv(path.join(path.dirname(path.dirname(getcwd())), "data/aggregate.csv"), index=False)

