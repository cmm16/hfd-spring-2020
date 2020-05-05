from scipy.stats.mstats import gmean
import numpy as np
from os.path import join, dirname
import pandas as pd
from os import getcwd

class CovidRiskCalculator:
    def __init__(self, dat, data_dir, save_path):
        dat['pct_elderly'] = dat["pctAdult4564"] + dat['pctAge65p']
        dat['health_pc'] = dat["health"] / dat['TotalPop']

        file2 = "percent_uninsured_block_group.csv"
        data_file2 = join(data_dir, file2)

        insurance = pd.read_csv(data_file2)
        insurance = insurance.rename(columns={"FIPS": "Block_Group",
                                              "% FINANCIAL SERVICES | HEALTH/LIFE INSURANCE | HEALTH/HOSPITAL/LIFE INSR-CURRENTLY HAVE | NO, 2019": "insurance"})

        dat = dat.merge(insurance, on="Block_Group")
        dat = dat.fillna(dat.median())


        self.dat = dat
        self.save_path = save_path


    def create_covid_df(self):
        self.dat['Poverty_Index'] = self.dat.apply(self.calculatePovertyIndex, axis=1)
        self.dat['Diversity_Index'] = self.dat.apply(self.calculateDiversityIndex, axis=1)
        self.dat['Health_Affliction_Index'] = self.dat.apply(self.calculateHealthAfflictionIndex, axis=1)

        # Normalize the Indicies to be 0-1
        self.dat['Health_Affliction_Index'] = ((self.dat['Health_Affliction_Index'] - self.dat['Health_Affliction_Index'].min())/(self.dat['Health_Affliction_Index'].max()-self.dat['Health_Affliction_Index'].min()))
        self.dat['Poverty_Index'] = ((self.dat['Poverty_Index'] - self.dat['Poverty_Index'].min())/(self.dat['Poverty_Index'].max()-self.dat['Poverty_Index'].min()))
        self.dat['Diversity_Index'] = ((self.dat['Diversity_Index'] - self.dat['Diversity_Index'].min())/(self.dat['Diversity_Index'].max()-self.dat['Diversity_Index'].min()))

        self.dat['Risk_Index'] = self.dat.apply(self.calculateRiskIndex, axis=1)

        indexDF = self.dat[["Block_Group", "Health_Affliction_Index", 'Poverty_Index','Diversity_Index', "Risk_Index"]]
        indexDF.to_csv(self.save_path, index=False)


    def calculatePovertyIndex(self, row):
        '''
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
        '''
        # print("____________________________________________")
        # print("Block Group")
        # print(row["Block_Group"])
        # print("____________________________________________")

        # List of Columns that go into the Prosperity Index
        criteriaHigh = ["pctFemHHwc", "pct_ltHS", "pct_lt30", "pctPubAsst", "pctBelow", "pct_gt1"]
        criteriaLow = ['pct_Prof_M', 'pct_Prof_F']

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
        '''
        Factors to calculate a neighborhood diversity index
        pctNHwht: Percentage white block group

        A high Diversity index (closer to 1)
        indicates a high number of Black or hispanic or other
        people
        in a block group
        '''
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
        '''
        Factors to calculate a Health Affliction index
        pct_elderly: Percent of People in age range 45+
        health_pc : health related calls per capita
        insurance: percent uninsured


        A high Health Affliction index (closer to 1)
        indicates more potential for sickness in a block group
        '''
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
        '''
        Factors to calculate a Risk index



        A high Health Affliction index (closer to 1)
        indicates more potential for sickness in a block group
        '''
        criteria = ["Health_Affliction_Index", 'Poverty_Index', 'Diversity_Index']

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

