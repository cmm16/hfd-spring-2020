import shapefile as shp
import json
import geopandas as gpd 
import folium
from folium import FeatureGroup, LayerControl, Map

def makeSingleBGMap(output_dir, geojson_filepath, geojson_key, map_filename, df, columns, legend_name, color="YlOrRd", bg=True):
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

