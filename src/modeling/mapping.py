import shapefile as shp
import json
import geopandas as gpd 
import folium
import branca
from folium import FeatureGroup, LayerControl, Map

callTypes = ['Fire','Health','Injuries External', 'Mental Illness', 'Motor', 'Other']
columns = ['Percent Fire Related Calls',
       'Percent Health Related Calls',
       'Percent Injuries External Related Calls',
       'Percent Mental Illness Related Calls', 'Percent Motor Related Calls',
       'Percent Other Related Calls', 'Predicted Percent Fire Related Calls',
       'Predicted Percent Health Related Calls',
       'Predicted Percent Injuries External Related Calls',
       'Predicted Percent Mental Illness Related Calls']


def run_map_maker(output_dir, data, bg_filepath, fd_filepath): 
    # Correct typo in data 
    data = data.rename({'Percent Other Calls':'Percent Other Related Calls', 
          'Pecent Motor Related Calls': 'Percent Motor Related Calls'}, axis=1)

    # Change block group to string type for mapping 
    data['Block_Group'] = data['Block_Group'].astype(str)
    data['Block_Group'] = data['Block_Group'].str[:12]

    # Make single maps 
    for column in callTypes: 
        print(column)
        formal_name = "Percent "+column+" Related Calls"
        makeSingleFDOutlineMap(output_dir, bg_filepath, fd_filepath, "feature.properties.Name", 
            "actual_"+column+"_blockGroup_map", data, formal_name, "Proportion of "+column+" Calls", column) 
        if column != 'Motor' and column != 'Other': 
            formal_name = "Predicted Percent "+column+" Related Calls"
            makeSingleFDOutlineMap(output_dir, bg_filepath, fd_filepath, "feature.properties.Name", 
                "predicted_"+column+"_blockGroup_map", data, formal_name, "Proportion of "+column+" Calls", column)            

    # Make mega interactive map 
    makeInteractiveMap(output_dir, data, bg_filepath, fd_filepath)


def make_bg_geo_data(bg_filepath, data): 
    bg_geo_df = gpd.read_file(bg_filepath, driver='GeoJSON')
    bg_geo_df = bg_geo_df[['Name', 'geometry']]
    bg_geo_data_df = bg_geo_df.merge(data, left_on='Name', right_on="Block_Group")
    return bg_geo_data_df


def makeSingleFDOutlineMap(output_dir, bg_filepath, fd_filepath, geojson_key, map_filename, data, 
    column, bg_info_col_name, casual_name, color="YlOrRd"): 
	"""
	Creates choloropleth map of single value with toggleable fire district outlines. 

	Inputs: 
	"""
	# Change block group to string type for mapping 
	data['Block_Group'] = data['Block_Group'].astype(str)
	data['Block_Group'] = data['Block_Group'].str[:12]

	fmap = folium.Map(location=[29.72, -95.60], tiles='cartodbpositron', zoom_start=10)

	folium.Choropleth(geo_data=bg_filepath, data=data, columns=['Block_Group', column], key_on=geojson_key, 
                    name=casual_name+" Map", fill_color=color, fill_opacity=1, line_opacity=0.2, 
                    nan_fill_color='White', legend_name=bg_info_col_name).add_to(fmap)

	style_function = lambda x: {'fillColor': '#ffffff', 'color':'black', 'fillOpacity': 0.1, 'weight': 2}
	highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.30, 'weight': 2}

    # Create data frame of admin dist to polygon 
	fd_geo_df = gpd.read_file(fd_filepath, driver='GeoJSON')
	fd_geo_df = fd_geo_df[['Fire_Districts.AdminDist', 'geometry']]

    # Add block group and fire district outlines
	folium.GeoJson(
        fd_geo_df, 
        show=False, 
        style_function = style_function,
        highlight_function = highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Fire_Districts.AdminDist'],
            aliases=['District Number'],
            localize=True
        ),
        name='Fire District').add_to(fmap)

	bg_geo_df = make_bg_geo_data(bg_filepath, data)
	folium.GeoJson(
        bg_geo_df, 
        highlight_function=highlight_function,
        style_function = lambda x: {
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['Block_Group', column],
            aliases=['Block Group', bg_info_col_name],
            localize=True
        ),
   		name='Block Group Information').add_to(fmap)

	LayerControl(collapsed=False).add_to(fmap)

	fmap.save(output_dir+"/"+map_filename+".html")  


def folium_del_legend(choropleth: folium.Choropleth):
    """A hack to remove choropleth legends.

    The choropleth color-scaled legend sometimes looks too crowded. Until there is an
    option to disable the legend, use this routine to remove any color map children
    from the choropleth.

    Args:
    choropleth: Choropleth objected created by `folium.Choropleth()`

    Returns:
    The same object `choropleth` with any child whose name starts with
    'color_map' removed.
    """
    del_list = []
    for child in choropleth._children:
        if child.startswith('color_map'):
            del_list.append(child)
    for del_item in del_list:
        choropleth._children.pop(del_item)
    return choropleth


def makeInteractiveMap(output_dir, data, bg_filepath, fd_filepath): 

    fmap = folium.Map(location=[29.72, -95.60], name="Map", tiles='cartodbpositron', 
                      zoom_start=10, control=False, overlay=False)

    for column in columns: 
        data[column] = data[column].round().astype(int)
        folium_del_legend(folium.Choropleth(geo_data=bg_filepath, 
                overlay=False, show = False, name=column, data=data, 
                threshold_scale = [0, 5, 10, 20, 30, 40, 50, 60, 80, 101],
                columns=['Block_Group', column], key_on='feature.properties.Name', 
                fill_color='YlOrRd', fill_opacity=1, line_opacity=0.2, 
                nan_fill_color='White', legend_name=column)).add_to(fmap)
                
    # Adds a legend - doesn't change existing values though 
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 90)
    colormap.caption = 'Proportion out of Total Calls'
    colormap.add_to(fmap)

    # Add block group outline 
    with open(bg_filepath) as f:
        bg = json.load(f)
    folium.GeoJson(
        bg, 
        style_function = lambda x: {
            'color': 'gray',
            'weight': 1,
            'fillOpacity': 0
        },
        name='Block Group Boundaries').add_to(fmap)

    style_function = lambda x: {'fillColor': '#ffffff', 'color':'black', 'fillOpacity': 0.1, 'weight': 2}
    highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.30, 'weight': 2}

    # Create data frame of admin dist to polygon 
    fd_geo_df = gpd.read_file(fd_filepath, driver='GeoJSON')
    fd_geo_df = fd_geo_df[['Fire_Districts.AdminDist', 'geometry']]

    # Add block group and fire district outlines
    folium.GeoJson(
        fd_geo_df, 
        show=False, 
        style_function = style_function,
        highlight_function = highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Fire_Districts.AdminDist'],
            aliases=['District Number'],
            localize=True
        ),
        name='Fire District').add_to(fmap)

    LayerControl(collapsed=False).add_to(fmap)

    fmap.save(output_dir+"/interactive-map.html")   

