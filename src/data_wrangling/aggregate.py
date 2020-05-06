import pandas as pd


def image_trend_aggregate(df):
    data = df.copy()
    data["Subcall_Code"] = data["Event_Type"].str[:4]
    data["Call_Category"] = data["Subcall_Code"].apply(lambda x: call_category_map[x])

    data = data.rename({"location": "Block_Group"}, axis=1)
    counts = data.groupby(["Block_Group", "Call_Category"]).size()
    counts = counts.unstack(level=1, fill_value=0).reset_index()
    return counts


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
    return counts.unstack(fill_value=0)


def aggregate(data_path, groupby_columns, save_path):
    df = pd.read_csv(data_path)
    df = compute_bg_column(df)
    aggregate_df = aggregate_call_type(df, groupby_columns)
    aggregate_df.to_csv(save_path)


call_category_map = {
    "FEAB": "health",
    "FEAV": "health",
    "FEBA": "health",
    "FECA": "health",
    "FECP": "health",
    "FEDI": "health",
    "FEHD": "health",
    "FEHV": "health",
    "FEHT": "health",
    "FEOB": "health",
    "FEPF": "health",
    "FEPV": "health",
    "FERE": "health",
    "FESE": "health",
    "FESI": "health",
    "FESV": "health",
    "FEST": "health",
    "FESY": "health",
    "FEUC": "health",
    "FEAR": "injuries_external",
    "FEVR": "injuries_external",
    "FEAS": "injuries_external",
    "FEBI": "injuries_external",
    "FEBL": "injuries_external",
    "FEBU": "injuries_external",
    "FECH": "injuries_external",
    "FEDR": "injuries_external",
    "FEEL": "injuries_external",
    "FEFA": "injuries_external",
    "FEFR": "injuries_external",
    "FEIJ": "injuries_external",
    "FEIN": "injuries_external",
    "FEPD": "injuries_external",
    "FEPO": "injuries_external",
    "FESG": "injuries_external",
    "FESH": "injuries_external",
    "FESW": "injuries_external",
    "FETA": "injuries_external",
    "FETE": "injuries_external",
    "FEMA": "motor",
    "FEMC": "motor",
    "FEAL": "mental_illness",
    "FEHG": "mental_illness",
    "FEOD": "mental_illness",
    "FEPS": "mental_illness",
    "FEUN": "other",
    "FEHZ": "other",
    "FEHU": "other",
    "FECK": "other",  # check patient
    "FEAM": "other",  # automatic alert
    "FEFD": "other",  # walk in
    "FESC": "other",  # HPD on scene
    "FEDA": "other",  # dead upon arrival
    "FEVJ": "other",  # fire stand by
    "FEAF": "other",  # assist the firefighter
    "FEET": "other",  # emergency transfer
    #### NEW MEDICAL CALLS ####
    "FEOF": "other",  # emergency assist the officer
    #### FIRE CALLS ####
    "FFDM": "fire",
    "FFGR": "fire",
    "FFTE": "fire",
    "FFAA": "fire",
    "FFOE": "fire",
    "FFMA": "fire",
    "FFHV": "fire",
    "FFLB": "fire",
    "FFMB": "fire",
    "FFEL": "fire",
    "FFUN": "fire",
    "FFSC": "fire",
    "FFSB": "fire",
    "FFHU": "fire",
    "FFGL": "fire",
    "FFCM": "fire",
    "FCON": "fire",
    "FMSC": "fire",
    "FFAL": "fire",
    "FFWR": "fire",
    "FFNO": "fire",
    "FFOR": "fire",
    "FFLV": "fire",
    "FFCH": "fire",
    "FFGN": "fire",
    "FFHR": "fire",
    "FFSP": "fire",
    "FFWD": "fire",
    "FHPD": "fire",
    "FFCL": "fire",
    "FFAF": "fire",
    "FFVJ": "fire",
    "FFTS": "fire",
    "FFCS": "fire",
    "FFTR": "fire",
    "FSCK": "fire",
    "FFSS": "fire",
    "FFHA": "fire",
    "FFBS": "fire",
    "FF31": "fire",
    "FF21": "fire",
    "FFAB": "fire",
    "FFES": "fire",
    "FFFW": "fire",
    "FFSH": "fire",
    "FPCK": "fire",
    "FFFD": "fire",
    "FF51": "fire",
    "FME": "fire",
    "FPDA": "fire",
    "FFPR": "fire",
    "FFSE": "fire",
    "FFAR": "fire",
    "FFPI": "fire",
    "FFAC": "fire",
    "FF41": "fire",
    "FFWA": "fire",
    "FFCO": "fire",
    "FTES": "other",
    "FSEV": "fire",
    "FPSE": "other",
    "FPSH": "other",
    "FPCP": "other",
    "FSTG": "fire",
    "FSHC": "fire",
    "NONE": "other",
    "FMP": "other",
    "F211": "other",
    "FMF": "other",
}
