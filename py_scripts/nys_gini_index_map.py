
# NYS GINI Index Analysis by Nicholas Kammerer
# Generates a Chloropleth map of NYS GINI Indices by County

#  Import appropriate libraries
import pandas as pd
import geopandas as gpd
import folium as fol
from branca.colormap import linear

#  Import overdose data and map data file paths.
data_path = "../data/nys_gini_coefficient_by_county.csv"
map_path = "../data/nys-counties.geojson"

#  Define info related to the data to be used in the visualization
title = "Wealth inequality per county, as measured by the GINI Index."

#  Read the overdose data into a pandas dataframe.
gini_by_county = pd.read_csv(data_path)

#  Read the NYS county data into a geopandas dataframe
nys_county_map = gpd.read_file(map_path)

#  Perform a join on the NYS county map dataframe and the overdose data dataframe
nys_county_map_gini_by_county = pd.merge(
    left=nys_county_map,
    right=gini_by_county,
    left_on='name',
    right_on='name'
)
nys_county_map_with_data_gdf = gpd.GeoDataFrame(nys_county_map_gini_by_county)

#  Create a Folium map centered on New York State
nys_county_gini_chloropleth_map = fol.Map(location=[42.917, -75.595], zoom_start=7)

#  Def a linear color scale for the overdoses
colormap = linear.BuPu_06.scale(nys_county_map_with_data_gdf['gini index'].min(),
                                nys_county_map_with_data_gdf['gini index'].max())

#  Adding the choropleth layer
fol.Choropleth(
    geo_data=nys_county_map_with_data_gdf,
    name='Choropleth',
    data=nys_county_map_with_data_gdf,
    columns=['name', 'gini index'],
    key_on='feature.properties.name',
    fill_color='YlOrBr',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=title,
    highlight=True
 ).add_to(nys_county_gini_chloropleth_map)

#  Adding a tooltip for each county
fol.features.GeoJson(
    nys_county_map_with_data_gdf,
    name='Labels',
    style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
    tooltip=fol.features.GeoJsonTooltip(
        fields=['name', 'gini index'],
        aliases=['County', 'Gini Index'],
        localize=True
    )
).add_to(nys_county_gini_chloropleth_map)

#  Display the map
nys_county_gini_chloropleth_map.save('../maps/interactive_nys_gini_index_map.html')
