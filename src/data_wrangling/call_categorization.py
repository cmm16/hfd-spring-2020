import pandas as pd 
from collections import defaultdict

"""
Default mapping of known call codes to category. 
This given mapping is based off the call codes Team HFD encountered and the 
manual categories we created. 
"""
call_category_map = {
### CAD CALL CODES ### 
'FEAB': 'health', 'FEAV': 'health', 'FEBA': 'health', 'FECA': 'health',
 'FECP': 'health', 'FEDI': 'health', 'FEHD': 'health', 'FEHV': 'health',
 'FEHT': 'health', 'FEOB': 'health', 'FEPF': 'health', 'FEPV': 'health',
 'FERE': 'health', 'FESE': 'health', 'FESI': 'health', 'FESV': 'health',
 'FEST': 'health', 'FESY': 'health', 'FEUC': 'health',
 'FEAR': 'injuries_external', 'FEVR': 'injuries_external',
 'FEAS': 'injuries_external', 'FEBI': 'injuries_external',
 'FEBL': 'injuries_external', 'FEBU': 'injuries_external',
 'FECH': 'injuries_external', 'FEDR': 'injuries_external',
 'FEEL': 'injuries_external', 'FEFA': 'injuries_external',
 'FEFR': 'injuries_external', 'FEIJ': 'injuries_external',
 'FEIN': 'injuries_external', 'FEPD': 'injuries_external',
 'FEPO': 'injuries_external', 'FESG': 'injuries_external',
 'FESH': 'injuries_external', 'FESW': 'injuries_external',
 'FETA': 'injuries_external', 'FETE': 'injuries_external',
 'FEMA': 'motor', 'FEMC': 'motor',
 'FEAL': 'mental_illness', 'FEHG': 'mental_illness',
 'FEOD': 'mental_illness', 'FEPS': 'mental_illness',
 'FEUN': 'other', 'FEHZ': 'other', 'FEHU': 'other', 
 'FECK': 'other', # check patient 
 'FEAM': 'other', # automatic alert 
 'FEFD': 'other', # walk in 
 'FESC': 'other', # HPD on scene 
 'FEDA': 'other', # dead upon arrival 
 'FEVJ': 'other', # fire stand by 
 'FEAF': 'other', # assist the firefighter 
 'FEET': 'other', # emergency transfer 
#### NEW MEDICAL CALLS ####  
'FEOF': 'other', # emergency assist the officer
#### FIRE CALLS ####
'FFDM': 'fire', 'FFGR': 'fire', 'FFTE': 'fire', 'FFAA': 'fire', 'FFOE': 'fire', 
'FFMA': 'fire', 'FFHV': 'fire', 'FFLB': 'fire', 'FFMB': 'fire', 'FFEL': 'fire', 
'FFUN': 'fire', 'FFSC': 'fire', 'FFSB': 'fire', 'FFHU': 'fire', 'FFGL': 'fire', 
'FFCM': 'fire', 'FCON': 'fire', 'FMSC': 'fire', 'FFAL': 'fire', 'FFWR': 'fire', 
'FFNO': 'fire', 'FFOR': 'fire', 'FFLV': 'fire', 'FFCH': 'fire', 'FFGN': 'fire', 
'FFHR': 'fire', 'FFSP': 'fire', 'FFWD': 'fire', 'FHPD': 'fire', 'FFCL': 'fire', 
'FFAF': 'fire', 'FFVJ': 'fire', 'FFTS': 'fire', 'FFCS': 'fire', 'FFTR': 'fire', 
'FSCK': 'fire', 'FFSS': 'fire', 'FFHA': 'fire', 'FFBS': 'fire', 'FF31': 'fire', 
'FF21': 'fire', 'FFAB': 'fire','FFES': 'fire', 'FFFW': 'fire', 'FFSH': 'fire', 
'FPCK': 'fire', 'FFFD': 'fire', 'FF51': 'fire', 'FME': 'fire', 'FPDA': 'fire', 
'FFPR': 'fire', 'FFSE': 'fire', 'FFAR': 'fire', 'FFPI': 'fire', 'FFAC': 'fire', 
'FF41': 'fire', 'FFWA': 'fire', 'FFCO': 'fire', 'FSEV': 'fire', 'FSHC': 'fire',
'FSTG': 'fire',
'FTES': 'other', 'FPSE': 'other', 'FPSH': 'other', 'FPCP': 'other', 
'NONE':'other', 'FMP':'other', 'F211':'other', 'FMF': 'other'
}

def getSubcall(df): 
 	"""
 	Takes an input data frame with a 6 digit call code and parses the 
 	call code into the first four letters. 

 	Input: data frame with 6 digit call code under column titled "Call_Type"

 	Returns: input data frame with a new column titled "Subcall_Type" with 
 		the four letter call code. 
 	"""
 	df['Subcall_Type'] = df['Call_Type'].str[:4]
 	return df 

def getCallCategories(df, mapping=call_category_map):
	"""
 	Categorizes each call entry in an inputted dataframe into a user defined 
 	category. If an unknown call code is encountered, will label the call 
 	as "unknown" category. 

 	Input: 
 		- df: the dataframe with 4 letter call code under column "Subcall_Type"
 		- mapping: a mapping of 4 letter call code to category. If not mapping
 			is specified, uses default created mapping 

 	Returns: input data frame with a new column titled "Call_Category" with 
 		the category for that row's call type. 

	"""
	df['Call_Category'] = df['Subcall_Type'].apply(lambda x: call_category_map[x] if x in call_category_map.keys() else "unknown")
	return df
