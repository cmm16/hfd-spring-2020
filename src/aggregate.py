"""
This function will group a dataframe by specified columns and 
count the number of entries in the specified groups. 
Inputs: 
    - df: the dataframe to perform calculations on 
    - groupby_columns: a list of the columns to group by 
Returns: a dataframe with the counts per group 
"""
def aggregate_call_type(df, groupby_columns): 
    counts = df.groupby(groupby_columns).size() 
    return counts.unstack(fill_value = 0)