import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests
import time  # For adding delay to respect API rate limits

import geopandas as gpd


database = r"C:\Users\l.dumarevskaya.ctr\ArcGIS projects\RISNER\data\CENSUS\Census_dataset\Census_dataset.gdb"


# Load a layer from a GeoPackage
Naloxon_survey = gpd.read_file(database, layer='NaloxonSurvey_GeocodeAddresses')
College_loc = gpd.read_file(database, layer='college_loc_XYTableToPoint')
Facilities = gpd.read_file(database, layer = 'Facilities_GeocodeAddresses')
Vending_machines = gpd.read_file(database, layer = 'Vending_GeocodeAddresses')


# Combine all datasets into one
combined_data = gpd.GeoDataFrame(
    pd.concat([College_loc, Naloxon_survey, Facilities, Vending_machines], ignore_index=True)
)

# Print the columns of the combined dataset
print("Columns in the combined dataset:", combined_data.columns.tolist())

# Print the first row of the combined dataset
print("\nFirst row of the combined dataset:")
print(combined_data.iloc[10])

# Save the combined dataset to a GeoPackage
combined_data.to_file(database, layer='Combined_All_Points', driver='GPKG')


# Extract coordinates from the geometry column
combined_data['x'] = combined_data.geometry.x
combined_data['y'] = combined_data.geometry.y

# Group by coordinates and count occurrences
duplicate_points = combined_data.groupby(['x', 'y']).size().reset_index(name='count')

# Filter points with more than one occurrence (i.e., duplicates)
duplicate_points = duplicate_points[duplicate_points['count'] > 1]

# Merge with the original dataset to get full details of duplicate points
duplicate_points_details = combined_data.merge(duplicate_points, on=['x', 'y'])

# Print the duplicate points
print("Duplicate Points:")
print(duplicate_points_details)

# Save the duplicate points to a new file (optional)
duplicate_points_details.to_file("duplicate_points.shp", driver='ESRI Shapefile')