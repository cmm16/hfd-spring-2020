import shapefile as shp
import json
import geopandas as gpd 
import folium
from folium import FeatureGroup, LayerControl, Map

def makeSingleBGMap(output_dir, geojson_filepath, geojson_key, map_filename, df, columns, legend_name, color="YlOrRd", bg=True):
    """
    Creates an interactive map of a single variable at block group level. 

    Inputs: 
        - output_dir: String path to output directory 
        - geojson_filepath: String path to block group geojson 
        - geojson_key: String key in geojson file to merge with block group in dataset
        - map_filename: String name of filename to save map to 
        - df: Dataframe with "Block_Group" column and other variable to plot
        - columns: array of string column names to plot 
        - legend_name: string name of legend 
        - color: string colorbrewer code 
        - bg: true if graphing results at block group level
    """
    if bg:
        # Make sure block group is string type for mapping 
        df['Block_Group'] = df['Block_Group'].astype(str)
        df['Block_Group'] = df['Block_Group'].str[:12]

    fmap = folium.Map(location=[29.72, -95.60], tiles='cartodbpositron', zoom_start=10)

    folium.Choropleth(geo_data=geojson_filepath, 
                    data=df, columns=columns, key_on=geojson_key, 
                    fill_color=color, fill_opacity=1, line_opacity=0.2, 
                    nan_fill_color='White', legend_name=legend_name).add_to(fmap)

    fmap.save(output_dir+"/"+map_filename+".html")  

