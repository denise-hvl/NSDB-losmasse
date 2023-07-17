import matplotlib.pyplot as plt
import pickle
import geopandas as gpd
import numpy as np
import pandas as pd
import contextily as ctx
#                   r"/home/chris/OneDrive/Impetus/Slushflow_db/Ele_sink_uphill.pickle"
df1 = pd.read_pickle("/home/chris/OneDrive/Impetus/Slushflow_db/Ele_sink_uphill.pickle")
grades = ['Godkjent kvalitet A', 'Godkjent kvalitet B'] #, "Godkjent kvalitet C"]


filtered_df = df1[df1['regStatus'].isin(grades)]
norway_path ="/home/chris/OneDrive/Impetus/Norway_shapefile/gadm41_NOR_0.shp"
norway = gpd.read_file(norway_path)
gdf_points = df1["geometry"].to_crs(epsg=4326)

# Plot the map of Norway
# Create subplots: one for the map and one for the histogram
fig, (ax_map, ax_hist) = plt.subplots(1, 2, figsize=(16, 8),sharey = True)

# Plot the basemap of Norway using contextily
norway = norway.to_crs(epsg=4326)  # Project to web mercator for the basemap
norway.plot(ax=ax_map, color='lightgray', edgecolor='black', alpha=0.7)
# Add Stamen Terrain basemap from contextily


#norway.plot(ax=ax, color='lightgray', edgecolor='black')

# Plot the points on the map
gdf_points.plot(ax=ax_map, color='red', markersize=5)

# Set plot title
ax_map.set_title('Map of Norway with Points')
ax_map.set_xlim([0, 35])
ax_map.set_ylim([57,72])
ax_hist.set_ylim([57,72])
ax_map.set_xlabel('Longitude')
# Show the plot
# Create a histogram of latitudes on the right axis (ax_hist)
latitudes = gdf_points.y
ax_hist.hist(latitudes, bins=20, edgecolor='black', color='blue',orientation="horizontal")
#ax_map.set_ylabel('Latitude')
ax_hist.set_xlabel('Frequency')
ax_hist.set_title('Histogram of Latitudes')
ax_hist.set_ylim([57,72])
plt.show()
"""
# Create a box plot using matplotlib
plt.figure(figsize=(8, 6))  # Optional: set the figure size

# Group the data by quality grade and plot the box plots
box_plot = filtered_df.boxplot(column='uphill potential_50', by='regStatus')

# Customize the plot
plt.title('Elevation (10 m raster) Box Plot by Quality Grade')
plt.xlabel('Quality Grade')
plt.ylabel('Uphill potential')
grade_string = ["Quality A"," Quality B","Quality C"]
box_plot.set_xticklabels(grade_string)
plt.suptitle('')  # Remove the default 'Boxplot grouped by...'
plt.show()
"""


# Create a figure and axes
fig, ax = plt.subplots()

# Plot histogram for elevation10
#ax.hist(filtered_df['elevation_10'], bins=25, alpha=0.5, label='Elevation 10')

# Plot histogram for elevation50
#ax.hist(filtered_df['elevation_50'], bins=25, alpha=0.5, label='Elevation 50')
bin_edges = list(range(0, 200, 5)) + [np.inf]
ax.hist([filtered_df['uphill potential_10'],filtered_df['max_uphill_50']], bins = bin_edges, label=["10m on point","Max from Neighbors "])
# Add labels, title, and legend
ax.set_xlabel('uphill potential (cells)')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of uphill potential (quality A and B)')
ax.legend()

# Show the plot
plt.show()
"""
latitude = df1["geometry"].y
latitude_filtered =filtered_df["geometry"].y
fig, ax = plt.subplots()

# Create a horizontal histogram
bin_width = 2
y_range = (55, 90)

# Create the horizontal histogram
ax.hist(latitude/100000, bins=range(y_range[0], y_range[1] + bin_width, bin_width), orientation='horizontal')

# Set the Y-axis range and label
ax.set_ylim(y_range)
ax.set_ylabel('Latitude [deg]')

# Set the X-axis label
ax.set_xlabel('Frequency')
ax.set_yticks([55, 59.0 ,60,63.4,65,69.6, 70,75,80,85,90])
ax.set_yticklabels([55, "Oslo" ,60,"Trondheim",65,"Tromsø", 70,75,80,85,90])
# Set the title
ax.set_title('Horizontal Histogram of Latitude')
"""

# Count the occurrences of 1 and 0 in the 'sinks' column
sink_counts50 = filtered_df['sinks_50'].value_counts()
sink_counts10 = filtered_df['sinks_50'].value_counts()
min_sink_counts50 = filtered_df['min_sinks_50'].value_counts()
min_sink_counts10 = filtered_df['min_sinks_50'].value_counts()
print(sink_counts50, sink_counts10, min_sink_counts10, min_sink_counts50)
# Create a bar plot


# Show the plot
plt.show()