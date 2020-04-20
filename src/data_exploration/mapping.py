import shapefile as shp
import folium
import json
from folium import plugins

def chloroplethMap(geojson_filepath, geojson_key, data, map_filename, columns, legend_name): 
	"""
	Function to create a chloropleth map. 

	Inputs: 
	- geojson_filepath: string filepath to geojson file 
	- geojson_key: geojson key to merge with data 
	- data: dataframe containing column of geographical unit and column of value to graph 
	- map_filename: string filename to save the map to (must end in .html)
	- columns: list of 2 column names - one of the geographical unit and one of the associated value 
	- legend_name: name of the value being graphed 

	Output: creates chloropleth to specified map_filename 
	"""
	# Read in geojson 
	with open(geojson_filepath) as f:
	    geojson = json.load(f)

	map = folium.Map(location=[29.72, -95.40], tiles='cartodbpositron', zoom_start=10)
	folium.GeoJson(geojson).add_to(map)
	map.choropleth(geo_data=geojson_filepath, data=data, columns=columns, 
		key_on=geojson_key, fill_color='PuRd', fill_opacity=1, 
		line_opacity=0.2, nan_fill_color='White', legend_name=legend_name)

	map.save(map_filename)