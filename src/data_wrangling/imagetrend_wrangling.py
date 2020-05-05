import pandas as pd 
from os.path import join, dirname

"""
Function that reads in a specified imagetrend csv file and 
converts the column titles into an understandable format. 

Input: string filepath to the imagetrend csv file 

Output: dataframe of the imagetrend data 
"""
def clean(filepath):
    df = pd.read_csv(filepath)
    df = df.rename({'Event_Number1':'Event_Number', 
                    'Entry_Date1': 'Entry_Date',
                    'Closed_Date1': 'Closed_Date',
                    'Event_Type1':'Event_Type', 
                    'Event_Description1':'Event_Description'}, axis=1)
    return df 

"""
Function that reads in multiple years of image trend data 
with a similar name and returns it as a single data frame. 

Input: 
- filepath_first_half: string of the first part of the file path 
- filepath_second_half: string of the second part of the file path 
- years: array of the years of the imagetrend data 

EXAMPLE: 
 filepath_first_half = "Jan thru Jun " 
 filepath_second_half = " - Event_Data_For_Rice_University (Rpt_Data_Rice_Events).csv"
 years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019"]

Output: dataframe of all the years of imagetrend data 
"""
def mergeYears(filepath_first_half, filepath_second_half, years):
    base = clean(filepath_first_half+years[0]+filepath_second_half)
    for year in years[1:]: 
        newdf = clean(filepath_first_half+year+filepath_second_half)
        base = pd.concat([base, newdf])
    return base 

"""
Function that parses the imagetrend incident Entry_Date field into a column 
for year, month, and date. 

Input: dataframe of imagetrend data with column "Entry_Date"

Output: modified dataframe with additional columns for year, month, and date 
"""
def parsetime(data): 
	data['parse'] = data['Entry_Date'].str.split()
	data[['parse','timestamp']] = pd.DataFrame(data.parse.values.tolist(), index=data.index)
	data['parse'] = data['parse'].str.split('-')
	data[['Year','Month', 'Date']] = pd.DataFrame(data.parse.values.tolist(), index= data.index)
	data = data.drop(['timestamp', 'parse'], axis=1)
	return data 

"""
Function that parses the imagetrend x and y coordinates into the correct 
order of magnitude.

Input: dataframe of imagetrend data with column "X_Coordinate" and "Y_Coordinate"

Output: modified dataframe with the correct order of magnitude for the two coordinates. 
"""
def parseCoordinates(data): 
	data['X_Coordinate'] = data['X_Coordinate']/1000000
	data['Y_Coordinate'] = data['Y_Coordinate']/1000000
	return data 

"""
Function that removes hobby and bush block groups. 

Returns: modified dataframe without any entries from hobby or bush.  
"""
def dropAirports(data):
	data = data[data['Block_Group']!=482019800001.0] # Hobby
	data = data[data['Block_Group']!=482019801001.0] # Bush
	return data 


def wrangle_image_trend(base_dir, save_dir):
    years = ["2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    end = " - Event_Data_For_Rice_University (Rpt_Data_Rice_Events).csv"

    pt1 = join(base_dir, "Jan thru Jun ")
    pt2 = join(base_dir, "Jul thru Dec ")

    df1 = mergeYears(pt1, end, years)
    df2 = mergeYears(pt2, end, years)
    df3 = pd.read_csv(join(base_dir,"Jan 1 2020 thru Apr 12 2020 - Event_Data_For_Rice_University (Rpt_Data_Rice_Events).csv"))
    df3 = df3.rename({'Event_Number1':'Event_Number',
                    'Entry_Date1': 'Entry_Date',
                    'Closed_Date1': 'Closed_Date',
                    'Event_Type1':'Event_Type',
                    'Event_Description1':'Event_Description'}, axis=1)

    df = pd.concat([df3, df2, df1]).drop(['Closed_Date'], axis=1)
    df = parsetime(df)
    df = parseCoordinates(df)
    df = df.dropna()
    df.to_csv(save_dir, index=False)

