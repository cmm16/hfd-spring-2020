from os.path import join
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import pymannkendall as mk

def run(output_dir, incidents_df):
	y20 = dataWrangling(incidents_df)
	plotTS(output_dir, y20, '3/1/2020', '4/12/2020')
	categories_df = plotCategories(output_dir, y20, '3/1/2020', '4/12/2020')
	trendTest(output_dir, categories_df)

def dataWrangling(incidents_df): 
	# Currently contains only calls from march and april 
	y20 = incidents_df[incidents_df['Year'] == 2020]
	y20 = y20[(y20['Month'] == 3) | (y20['Month'] == 4)]
	return y20

def plotTS(output_dir, data, start_date, end_date):
    counts = data.groupby(['Month','Date']).count()['Event_Number'].unstack(0)
    
    # Flatten data frame into single column
    all_data = counts.values.flatten(order='F')
    flat_data = all_data[~np.isnan(all_data)]

    # Data frame for graphing
    drange = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame(flat_data, index=drange)
    plt.rc('figure', figsize=(12, 8))

    fig, ax = plt.subplots()
    ax.plot(df.index, df.values)
    plt.title("Daily Calls", fontsize=20)
    plt.ylabel('Call Count', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.savefig(join(output_dir, "daily_calls_during_covid.png"))
    plt.close()

def makeSingle(data): 
    counts = data.groupby(['Month','Date']).count()['Event_Number'].unstack(0)
    # Flatten data frame into single column
    all_data = counts.values.flatten(order='F')
    flat_data = all_data[~np.isnan(all_data)]
    return flat_data

def plotCategories(output_dir, data, start_date, end_date): 
	motor = data[data['Call_Category']=='motor']
	m1 = makeSingle(motor)
	health = data[data['Call_Category']=='health']
	h1 = makeSingle(health)
	injuries = data[data['Call_Category']=='injuries_external']
	ie1 = makeSingle(injuries)
	other = data[data['Call_Category']=='other']
	o1 = makeSingle(other)
	mental_illness = data[data['Call_Category']=='mental_illness']
	mi1 = makeSingle(mental_illness)
	fire = data[data['Call_Category']=='fire']
	f1 = makeSingle(mental_illness)

	drange = pd.date_range(start=start_date, end=end_date)
	df = pd.DataFrame({'motor':m1, 'health': h1, 'injuries_external':ie1, 
	                   'other': o1, 'mental_illness': mi1, 'fire': f1}, index=drange)

	df.plot();
	plt.title("Daily Calls", fontsize=20)
	plt.xlabel('Date', fontsize=18)
	plt.xticks(fontsize=16)
	plt.ylabel("Number of Calls", fontsize=18)
	plt.yticks(fontsize=16)
	plt.savefig(join(output_dir, "daily_call_categories_during_covid.png"))
	plt.close()
	return df

def trendTest(output_dir, data): 
	call_categories = ['injuries_external', 'motor', 'health', 'fire', 'mental_illness', 'other']
	trend = []
	h = []
	p = []
	z =[]
	Tau = []
	s = []
	var_s = []
	slope = []

	for category in call_categories: 
	    category_data = data[[category]]
	    to, ho, po, zo, Tauo, so, var_so, slopeo = mk.original_test(category_data)
	    trend.append(to)
	    h.append(ho)
	    p.append(po)
	    z.append(zo)
	    Tau.append(Tauo)
	    s.append(so)
	    var_s.append(var_so)
	    slope.append(slopeo)
	    
	results = pd.DataFrame({'Call_Category':call_categories, 'Trend':trend, 'h':h, 'p':p,
	                       'z':z, 'Tau':Tau, 's':s, 'var_s':var_s, 'slope':slope})
	results.to_csv(join(output_dir, "trend_test_results.csv"), index=False)

