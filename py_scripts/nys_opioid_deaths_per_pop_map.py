
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
title = "Percent of the population experiencing a fatal overdose, per county, 2020."

#  Read the overdose data into a pandas dataframe.
overdoses_by_county = pd.read_csv(data_path)

# Clean commas from population column
overdoses_by_county["population"] = overdoses_by_county["population"].replace(',', '', regex=True)

# Convert population from str to int
overdoses_by_county = overdoses_by_county.astype({'population': 'int'})

# Calculates Overdose rate, populated from Overdoses/Population
overdoses_by_county['od rate'] = overdoses_by_county['overdoses'] / overdoses_by_county['population']

# Calculates overdose rate percent (for visualization)
overdoses_by_county['od rate percent'] = (overdoses_by_county['overdoses'] / overdoses_by_county['population']) * 100

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
colormap = linear.YlOrRd_09.scale(nys_county_map_with_data_gdf['od rate'].min(),
                                  nys_county_map_with_data_gdf['od rate'].max())

#  Adding the choropleth layer
fol.Choropleth(
    geo_data=nys_county_map_with_data_gdf,
    name='Choropleth',
    data=nys_county_map_with_data_gdf,
    columns=['name', 'od rate percent'],
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
        fields=['name', 'overdoses', 'population', 'od rate percent'],
        aliases=['County', 'Overdoses', 'Population', 'Overdose Rate (%)'],
        localize=True
    )
).add_to(nys_county_overdose_chloropleth_map)

#  Display the map
nys_county_overdose_chloropleth_map.save('../maps/interactive_nys_opioid_deaths_per_pop_map.html')
