import shapefile as shp
import json
import geopandas as gpd 
import folium
from folium import FeatureGroup, LayerControl, Map

def make_bg_geo_data(bg_filepath, data, bg_column_name): 
	bg_geo_df = gpd.read_file(bg_filepath, driver='GeoJSON')
	bg_geo_df = bg_geo_df[[bg_data_col_name, 'geometry']]
	bg_geo_data_df = bg_geo_df.merge(data, left_on=bg_data_col_name, right_on="Block_Group")
	return bg_geo_data_df

def makeSingleBGMap(output_dir, bg_filepath, geojson_key, map_filename, df, columns, legend_name, color="YlOrRd"):
    # Change block group to string type for mapping 
    df['Block_Group'] = df['Block_Group'].astype(str)
    df['Block_Group'] = df['Block_Group'].str[:12]

    fmap = folium.Map(location=[29.72, -95.60], tiles='cartodbpositron', zoom_start=10)

    folium.Choropleth(geo_data=bg_filepath, 
                    data=df, columns=columns, key_on=geojson_key, 
                    fill_color=color, fill_opacity=1, line_opacity=0.2, 
                    nan_fill_color='White', legend_name=legend_name).add_to(fmap)

    fmap.save(output_dir+"/"+map_filename+".html")  

def makeSingleFDOutlineMap(output_dir, bg_filepath, fd_filepath, geojson_key, map_filename, data, 
    columns, legend_name, bg_info_col, bg_info_col_name, bg_data_col_name, color="YlOrRd", mapname="Map"): 
	"""
	Creates choloropleth map of single value with toggleable fire district outlines. 

	Inputs: 
	"""
	# Change block group to string type for mapping 
	data['Block_Group'] = data['Block_Group'].astype(str)
	data['Block_Group'] = data['Block_Group'].str[:12]

	fmap = folium.Map(location=[29.72, -95.60], tiles='cartodbpositron', zoom_start=10)

	folium.Choropleth(geo_data=bg_filepath, data=data, columns=columns, key_on=geojson_key, 
                    name=mapname, fill_color=color, fill_opacity=1, line_opacity=0.2, 
                    nan_fill_color='White', legend_name=legend_name).add_to(fmap)

	style_function = lambda x: {'fillColor': '#ffffff', 'color':'black', 'fillOpacity': 0.1, 'weight': 2}
	highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.30, 'weight': 2}

    # Create data frame of admin dist to polygon 
	nbh_geo_df = gpd.read_file(fd_filepath, driver='GeoJSON')
	nbh_geo_df = nbh_geo_df[['Fire_Districts.AdminDist', 'geometry']]

    # Add block group and fire district outlines
	folium.GeoJson(
        nbh_geo_df, 
        style_function = style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Fire_Districts.AdminDist'],
            aliases=['District Number'],
            localize=True
        ),
        name='Fire District').add_to(fmap)

	bg_geo_data = make_bg_geo_data(bg_filepath, data, bg_data_col_name)
	folium.GeoJson(
        bg_geo_data_df, 
        highlight_function=highlight_function,
        style_function = lambda x: {
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['BG_ID', bg_info_col],
            aliases=['Block Group', bg_info_col_name],
            localize=True
        ),
   		name='Block Group Information').add_to(fmap)

	LayerControl(collapsed=False).add_to(fmap)

	fmap.save(output_dir+"/"+map_filename+".html")  

