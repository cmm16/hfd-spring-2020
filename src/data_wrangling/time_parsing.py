def parseDates(df):
	"""
	Parses an incident id into 

	Input: a data frame with incident id where incident id format 
		is YYMMDDseqx. ** NOTE: The column name must be titled "Incident_ID" **
	
	Returns: the same data frame with 4 new columns titled Year, Month, Date, 
		Incident. 
	"""
	df["inc_string"] = df["Incident_ID"].apply(str)

	# Incident ID format = YYMMDDseqx
	df["Year"] = ("20" + df["inc_string"].str[:2]).astype(int)
	df["Month"] = df["inc_string"].str[2:4].astype(int)
	df["Date"] = df["inc_string"].str[4:6].astype(int)
	df["Incident"] = df["inc_string"].str[6:11].astype(int)
	return df
