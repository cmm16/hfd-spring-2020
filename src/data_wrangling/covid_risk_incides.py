from os.path import join

import numpy as np
import pandas as pd
from scipy.stats.mstats import gmean


class CovidRiskCalculator:
    def __init__(self, dat, call_counts, data_dir, save_path):
        dat["pct_elderly"] = dat["pctAdult4564"] + dat["pctAge65p"]
        dat["health_pc"] = dat["health"] / dat["TotalPop"]

        file2 = "percent_uninsured_block_group.csv"
        data_file2 = join(data_dir, file2)

        insurance = pd.read_csv(data_file2)
        insurance = insurance.rename(
            columns={
                "FIPS": "Block_Group",
                "% FINANCIAL SERVICES | HEALTH/LIFE INSURANCE | HEALTH/HOSPITAL/LIFE INSR-CURRENTLY HAVE | NO, 2019": "insurance",
            }
        )
        dat = dat.merge(insurance, on="Block_Group")
        dat = dat.fillna(dat.median())
        call_counts = call_counts.loc[dat.set_index("Block_Group").index, :]
        dat[
            ["fire", "health", "injuries_external", "mental_illness", "motor", "other"]
        ] = call_counts.values

        self.dat = dat
        self.save_path = save_path

    def create_covid_df(self):
        self.dat["Poverty_Index"] = self.dat.apply(self.calculatePovertyIndex, axis=1)
        self.dat["Diversity_Index"] = self.dat.apply(
            self.calculateDiversityIndex, axis=1
        )
        self.dat["Health_Affliction_Index"] = self.dat.apply(
            self.calculateHealthAfflictionIndex, axis=1
        )

        # Normalize the Indicies to be 0-1
        self.dat["Health_Affliction_Index"] = (
            self.dat["Health_Affliction_Index"]
            - self.dat["Health_Affliction_Index"].min()
        ) / (
            self.dat["Health_Affliction_Index"].max()
            - self.dat["Health_Affliction_Index"].min()
        )
        self.dat["Poverty_Index"] = (
            self.dat["Poverty_Index"] - self.dat["Poverty_Index"].min()
        ) / (self.dat["Poverty_Index"].max() - self.dat["Poverty_Index"].min())
        self.dat["Diversity_Index"] = (
            self.dat["Diversity_Index"] - self.dat["Diversity_Index"].min()
        ) / (self.dat["Diversity_Index"].max() - self.dat["Diversity_Index"].min())

        self.dat["Risk_Index"] = self.dat.apply(self.calculateRiskIndex, axis=1)
        indexDF = self.dat[
            [
                "Block_Group",
                "Health_Affliction_Index",
                "Poverty_Index",
                "Diversity_Index",
                "Risk_Index",
            ]
            + [
                "fire",
                "health",
                "injuries_external",
                "mental_illness",
                "motor",
                "other",
            ]
        ]
        indexDF.to_csv(self.save_path, index=False)

    def calculatePovertyIndex(self, row):
        """
         Factors considered come from the neighborhood deprivation index
        "pctFemHHwc" : % Single Mothers, higher = poorer
        "pct_ltHS": % Of people without high school diploma, higher = poorer
        "pct_Prof_M": % Men In skilled position, lower = poorer
        "pct_Prof_F": % Female In skilled position, lower = poorer
        "pct_lt30": % of households with yearly income less than 30,000, higher = Poorer
        "pctPubAsst": % Public assistance income, higher = poorer.
        "pctBelow": % Percent of people below the poverty line, higher = poorer
        "pct_gt1": A crowededness index, higher = poorer

        A high poverty index (closer to 1) indicates a poorer block group
        """
        # print("____________________________________________")
        # print("Block Group")
        # print(row["Block_Group"])
        # print("____________________________________________")

        # List of Columns that go into the Prosperity Index
        criteriaHigh = [
            "pctFemHHwc",
            "pct_ltHS",
            "pct_lt30",
            "pctPubAsst",
            "pctBelow",
            "pct_gt1",
        ]
        criteriaLow = ["pct_Prof_M", "pct_Prof_F"]

        # List of indiviudal Indicies (0, 1) for each column
        indicies = []

        for criterion in criteriaHigh:
            maximum = self.dat[criterion].max()
            minimum = self.dat[criterion].min()
            index = (row[criterion] - minimum) / (maximum - minimum)
            indicies.append(index)

        for criterion in criteriaLow:
            maximum = self.dat[criterion].max()
            minimum = self.dat[criterion].min()
            index = (row[criterion] - minimum) / (maximum - minimum)
            indicies.append(1 - index)

        # poverty_index = gmean(indicies)
        poverty_index = np.mean(indicies)

        return poverty_index

    def calculateDiversityIndex(self, row):
        """
        Factors to calculate a neighborhood diversity index
        pctNHwht: Percentage white block group

        A high Diversity index (closer to 1)
        indicates a high number of Black or hispanic or other
        people
        in a block group
        """
        # criteria = ["pctHisp", "pctNHblk", "pctNHoth"]
        criteria = ["pctNHwht"]

        # List of indiviudal Indicies (0, 1) for each column
        indicies = []

        for criterion in criteria:
            maximum = self.dat[criterion].max()
            minimum = self.dat[criterion].min()
            index = (row[criterion] - minimum) / (maximum - minimum)
            # indicies.append(index)
            indicies.append(1 - index)

        # diversity_index = gmean(indicies)
        diversity_index = np.mean(indicies)

        return diversity_index

    def calculateHealthAfflictionIndex(self, row):
        """
        Factors to calculate a Health Affliction index
        pct_elderly: Percent of People in age range 45+
        health_pc : health related calls per capita
        insurance: percent uninsured


        A high Health Affliction index (closer to 1)
        indicates more potential for sickness in a block group
        """
        criteria = ["pct_elderly", "health_pc", "insurance"]

        # List of indiviudal Indicies (0, 1) for each column
        indicies = []

        for criterion in criteria:
            maximum = self.dat[criterion].max()
            minimum = self.dat[criterion].min()
            index = (row[criterion] - minimum) / (maximum - minimum)
            indicies.append(index)

        # diversity_index = gmean(indicies)
        health_affliction_index = np.mean(indicies)

        return health_affliction_index

    def calculateRiskIndex(self, row):
        """
        Factors to calculate a Risk index



        A high Health Affliction index (closer to 1)
        indicates more potential for sickness in a block group
        """
        criteria = ["Health_Affliction_Index", "Poverty_Index", "Diversity_Index"]

        # List of indiviudal Indicies (0, 1) for each column
        indicies = []

        for criterion in criteria:
            maximum = self.dat[criterion].max()
            minimum = self.dat[criterion].min()
            index = (row[criterion] - minimum) / (maximum - minimum)
            indicies.append(index)

        risk = gmean(indicies)
        # risk = np.mean(indicies)

        return risk


def aggregate_covid_to_fire_dist(df, covid_df, save_path):
    df1 = df.groupby(["AdminDist", "Name"]).count()[["Event_Number"]].reset_index()
    df2 = df.groupby(["AdminDist"]).count()[["Event_Number"]].reset_index()
    df3 = df1.merge(df2, how="left", left_on="AdminDist", right_on="AdminDist")
    df3["scaler"] = df3["Event_Number_x"] / df3["Event_Number_y"]

    merged_df = covid_df.merge(df3, how="inner", left_on="Block_Group", right_on="Name")
    indices_to_scale = ["Health_Affliction_Index", "Poverty_Index", "Diversity_Index"]
    call_types = [
        "fire",
        "health",
        "injuries_external",
        "mental_illness",
        "motor",
        "other",
    ]
    merged_df["call_prob"] = merged_df[call_types].sum(1) / sum(
        merged_df[call_types].sum(1)
    )

    for col in indices_to_scale:
        merged_df[col] = merged_df[col] * merged_df["scaler"]
    new_df = merged_df[call_types + ["scaler", "AdminDist", "call_prob"]]
    # replace with save path
    new_df.groupby(["AdminDist"]).sum().reset_index().to_csv(save_path)
