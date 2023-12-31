
# NYS Opioid Epidemic Analysis by Nicholas Kammerer
# Generates a Chloropleth map of NYS Opioid Overdoses by County

#  Import appropriate libraries
import pandas as pd
import geopandas as gpd
import folium as fol
from branca.colormap import linear

#  Import overdose data and map data file paths.
data_path = "../data/nys_overdose_deaths_involving_opioids_by_county.csv"
map_path = "../data/nys-counties.geojson"

#  Define info related to the data to be used in the visualization
data_source = "Vital Statistics Data as of November 2022"
data_year = "2020"
title = "Overdose deaths involving opioids per county, " + data_year + "."

#  Read the overdose data into a pandas dataframe.
overdoses_by_county = pd.read_csv(data_path)

#  Read the NYS county data into a geopandas dataframe
nys_county_map = gpd.read_file(map_path)

#  Perform a join on the NYS county map dataframe and the overdose data dataframe
nys_county_map_overdoses_by_county = pd.merge(
    left=nys_county_map,
    right=overdoses_by_county,
    left_on='name',
    right_on='name'
)
nys_county_map_with_data_gdf = gpd.GeoDataFrame(nys_county_map_overdoses_by_county)

#  Create a Folium map centered on New York State
nys_county_overdose_chloropleth_map = fol.Map(location=[42.917, -75.595], zoom_start=7)

#  Def a linear color scale for the overdoses
colormap = linear.YlOrRd_09.scale(nys_county_map_with_data_gdf['overdoses'].min(),
                                  nys_county_map_with_data_gdf['overdoses'].max())

#  Adding the choropleth layer
fol.Choropleth(
    geo_data=nys_county_map_with_data_gdf,
    name='Choropleth',
    data=nys_county_map_with_data_gdf,
    columns=['name', 'overdoses'],
    key_on='feature.properties.name',
    fill_color='Reds',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=title,
    highlight=True
 ).add_to(nys_county_overdose_chloropleth_map)

#  Adding a tooltip for each county
fol.features.GeoJson(
    nys_county_map_with_data_gdf,
    name='Labels',
    style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
    tooltip=fol.features.GeoJsonTooltip(
        fields=['name', 'overdoses', 'population'],
        aliases=['County', 'Overdoses', 'Population'],
        localize=True
    )
).add_to(nys_county_overdose_chloropleth_map)

#  Display the map
nys_county_overdose_chloropleth_map.save('../maps/interactive_nys_opioid_overdose_map.html')
