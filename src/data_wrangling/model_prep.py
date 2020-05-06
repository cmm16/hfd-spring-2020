from os.path import join

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None



def combine_demographic_features(df):
    """
    combines existing demographic features and selects others for new feature engineered predictor variable data frame

    Arguments:
        df (DataFrame): data frame containing demographic data

    Returns:
         new data frame of few and condensed features
    """
    new_df = df[["Block_Group"]]

    # Age
    new_df["pctMinor"] = df.loc[:, "pctAge0017"]
    new_df["pctAdult"] = (
        100.0 * df.loc[:, "TotPop18"] / df.loc[:, "TotalPop"]
    ) - df.loc[:, "pctAge65p"]
    new_df["pctElderly"] = df.loc[:, "pctAge65p"]
    new_df["aveAge"] = (df.loc[:, "Age00_04"] / df.loc[:, "TotalPop"] * 2) + (
        (df.loc[:, "Age05_17"] / df.loc[:, "TotalPop"] * 11)
        + (df.loc[:, "Age18_21"] / df.loc[:, "TotalPop"] * 19.5)
        + (df.loc[:, "Age22_29"] / df.loc[:, "TotalPop"] * 25.5)
        + (df.loc[:, "Age30_39"] / df.loc[:, "TotalPop"] * 34.5)
        + (df.loc[:, "Age40_49"] / df.loc[:, "TotalPop"] * 44.5)
        + (df.loc[:, "Age50_64"] / df.loc[:, "TotalPop"] * 57)
        + (df.loc[:, "Age65p"] / df.loc[:, "TotalPop"] * 72)
    )

    # Gender
    # new_df['pctFem'] = df['pctFem']
    new_df["pctMale"] = df["pctMale"]

    # Ethnicity/Race
    new_df["pctHisp"] = df["pctHisp"]
    new_df["pctNHasi"] = df["pctNHasi"]
    new_df["pctNHblk"] = df["pctNHblk"]
    new_df["pctNHoth"] = df["pctNHoth"]
    new_df["pctNHwht"] = df["pctNHwht"]
    new_df["raceVar"] = np.var(
        df[["pctHisp", "pctNHasi", "pctNHblk", "pctNHblk", "pctNHoth", "pctNHwht"]], 1
    )  # race variance

    # Education
    new_df["pct_ltHS"] = df["pct_ltHS"]
    new_df["pct_HS"] = df["pct_HS"]
    new_df["pct_Coll"] = df["pct_Coll"] - df["pct_MA"]  # just college
    new_df["pct_grad"] = df["pct_MA"]
    new_df["eduVar"] = np.var(
        new_df[["pct_ltHS", "pct_HS", "pct_Coll", "pct_grad"]], 1
    )  # education variance

    # Poverty
    new_df["pctBelow"] = df["pctBelow"]
    new_df["TotPovLev"] = df["TotPovLev"]

    # Employment
    new_df["pctDiffMFEmp"] = (
        df["pct_Prof_M"] - df["pct_Prof_F"]
    )  # Percent difference of male female employment

    # Housing
    new_df["HUperHH"] = df["TotHU"] / df["TotHH"]  # housing units per house holds
    new_df["pctOccup"] = df["pctOccup"]
    new_df["pctOwn"] = df["pctOwn"]
    new_df["pct_lt1"] = df["pct_lt1"]
    new_df["q1_HUval"] = df["Q1_HUval"]
    new_df["medHUval"] = df["medHUval"]
    new_df["Q3_HUval"] = df["Q3_HUval"]

    # Households
    new_df["HHperPop"] = df["TotHH"] / df["TotalPop"]
    new_df["pct_gt75"] = df["pct_gt75"]
    new_df["medHHinc"] = df["medHHinc"]
    new_df["pctPubAsst"] = df["pctPubAsst"]
    new_df["pctIntDiv"] = df["pctIntDiv"]

    new_df["FamperHH"] = df["TotFamily"]
    new_df["pctFemHH"] = df["pctFemHH"]

    # lang
    new_df["pctLangNEngl"] = df["pctLangNEngl"]

    # commute
    new_df["pctWorkHome"] = df["pctWorkHome"]
    new_df["estCommTime"] = (
        (df.pctComm00_14 * 7)
        + (df.pctComm15_29 * 22)
        + (df.pctComm30_59 * 44.5)
        + (df.pctComm60p * 70)
    )

    # Added
    #new_df["Acres"] = df.Acres
    #new_df["Near_Station_Number"] = df.Near_Station_Number
    #new_df["Center_X"] = df.Center_X
    #new_df["Center_Y"] = df.Center_Y
    #new_df["Intersections"] = df.Intersections

    new_df = new_df.set_index("Block_Group")

    return new_df


def table_joins(data_dir, initial_df):
    """
    Joins all wrangled tables together. 
    Inputs: 
        - data_dir: string path to data directory
        - initial_df: string path to initial data frame (for skip command)
    """
    """ Joins feature engineered data frame to additional data sets for new features """
    df_acres = pd.read_csv(join(data_dir,"acres.csv"))
    df_fire_station = pd.read_csv(join(data_dir,"centroid_nearest_firestation_censusblockgroup.csv"))
    intersections_df = pd.read_excel(join(data_dir,"Intersection_SpatialJoin_BlockGroup.xls"))

    intersections_df = (
        intersections_df.groupby("BlockGroup")
        .count()
        .reset_index()[["BlockGroup", "OBJECTID"]]
        .rename({"OBJECTID": "Intersections"}, axis=1)
    )
    df = initial_df.merge(
        df_acres[["Block_Group", "Acres"]],
        how="inner",
        left_on="Block_Group",
        right_on="Block_Group",
    )
    df = df.merge(
        df_fire_station[
            ["Name", "FIPS_Poly_Cen_x", "FIPS_Poly_Cen_y", "Near_Station_Number"]
        ],
        how="inner",
        left_on="Block_Group",
        right_on="Name",
    ).drop(["Name"], axis=1)
    df = df.rename(
        {"FIPS_Poly_Cen_x": "Center_X", "FIPS_Poly_Cen_y": "Center_Y"}, axis=1
    )
    df = df.merge(
        intersections_df, how="left", left_on="Block_Group", right_on="BlockGroup"
    ).drop(["BlockGroup"], axis=1)
    # df = pd.read_csv("/Users/work/PycharmProjects/hfd-spring-2020/data/train_categories.csv")

    return df


def remove_nulls(df):
    """ 
    Replaces all non-existing values in data frame with its columns median value 
    """
    for col in df.columns:
        df[col].fillna((df[col].median()), inplace=True)
    return df


def create_targets_df(df, intial_df):
    """ 
    Creates target data frame converting counts of call categories per block group to percents per block group 
    """
    target_df = intial_df[
        [
            "Block_Group",
            "fire",
            "health",
            "injuries_external",
            "mental_illness",
            "motor",
            "other",
        ]
    ].set_index("Block_Group")
    target_df = target_df.loc[df.index, :]

    target_df["total_calls"] = target_df.sum(1)
    for col in [
        "fire",
        "health",
        "injuries_external",
        "mental_illness",
        "motor",
        "other",
    ]:
        target_df["per_" + col] = 100 * ((target_df[col]) / target_df["total_calls"])
    target_df = target_df.rename(
        {
            "per_fire": "Percent Fire Related Calls",
            "per_health": "Percent Health Related Calls",
            "per_injuries_external": "Percent Injuries External Related Calls",
            "per_mental_illness": "Percent Mental Illness Related Calls",
            "per_motor": "Pecent Motor Related Calls",
            "per_other": "Percent Other Calls",
        },
        axis=1,
    )

    target_df = target_df.drop(
        [
            "fire",
            "health",
            "injuries_external",
            "mental_illness",
            "motor",
            "other",
            "total_calls",
        ],
        axis=1,
    )
    return target_df


def model_prep(data_dir, initial_df):
    """ 
    Combines all functions necessary to prepare data from modeling going but before test train split 
    """
    df = combine_demographic_features(initial_df)
    df = remove_nulls(df)
    target_df = create_targets_df(df, initial_df)

    dem_only_preds = df.copy()

    dem_only_preds.to_csv("dem_only_preds.csv")
    df.to_csv("all_preds.csv")
    target_df.to_csv("target.csv")

    return dem_only_preds, df, target_df
