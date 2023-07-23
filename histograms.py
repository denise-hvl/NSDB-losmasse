import matplotlib.pyplot as plt
import pickle
import geopandas as gpd
import numpy as np
import pandas as pd
import contextily as ctx


def Map_plot(filtered_df):
    norway_path ="/home/chris/OneDrive/Impetus/Norway_shapefile/gadm41_NOR_0.shp"

    norway = gpd.read_file(norway_path)
    gdf_points = df1["geometry"].to_crs(epsg=4326)
    filtered_df = filtered_df["geometry"].to_crs(epsg=4326)
    sub_arctic =filtered_df[filtered_df.y < 65]
    print( "not arctic ", len(sub_arctic), len(filtered_df))
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
    ax_map.set_title('Map of Norway with Points', fontsize = 24)
    ax_map.set_xlim([0, 35])
    ax_map.set_ylim([57,72])
    ax_hist.set_ylim([57,72])
    ax_map.set_xlabel('Longitude', fontsize = 20)
    ax_map.set_ylabel("Latitude", fontsize = 20)
    # Show the plot
    # Create a histogram of latitudes on the right axis (ax_hist)
    latitudes = gdf_points.y
    ax_hist.hist(latitudes, bins=20, edgecolor='black', color='blue',orientation="horizontal")
    #ax_map.set_ylabel('Latitude')
    ax_hist.set_xlabel('Frequency', fontsize = 20)
    ax_hist.set_title('Histogram of Latitudes', fontsize = 24)
    ax_map.tick_params(axis='both', which='major', labelsize=20)
    ax_hist.tick_params(axis='both', which='major', labelsize=20)
    #ax.tick_params(axis='both', which='minor', labelsize=8)
    ax_hist.set_ylim([57,72])
    fig.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/map_of_events.png")
    plt.show()

def slopes_box_plot(filter_df):
    # Create a box plot using matplotlib
    # Group the data by quality grade and plot the box plots
    box_plot = filtered_df.boxplot(column='slopes_10', by='regStatus')

    # Customize the plot
    plt.title('Slopes Box Plot by Quality Grade')
    plt.xlabel('Quality Grade')
    plt.ylabel('Slopes')
    grade_string = ["Quality A"," Quality B","Quality C"]
    box_plot.set_xticklabels(grade_string)
    plt.suptitle('')  # Remove the default 'Boxplot grouped by...'

def up_hilll_hist(filtered_df):
    # uphill potential plot
    fig, ax = plt.subplots()

    bin_edges = list(range(0, 200, 5)) + [np.inf]
    ax.hist([filtered_df['uphill potential_10'],filtered_df['max_uphill_50']], bins = bin_edges, label=["10m on point","Max from Neighbors "])
    # Add labels, title, and legend
    ax.set_xlabel('uphill potential (cells)')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of uphill potential (quality A and B)')
    ax.legend()

    fig1, ax1 = plt.subplots()
    dfA = df1[df1['regStatus'] == 'Godkjent kvalitet A']
    dfB = df1[df1['regStatus'] == 'Godkjent kvalitet B']
    dfC = df1[df1['regStatus'] == 'Godkjent kvalitet C']
    ax1.scatter(dfC["elevation_10"], dfC["slopes_10"], label = "Quality C")
    ax1.scatter(dfB["elevation_10"], dfB["slopes_10"], label = "Quality B")
    ax1.scatter(dfA["elevation_10"], dfA["slopes_10"], label = "Quality A")
    ax1.set_xlabel('Elevation [m]')
    ax1.set_ylabel('Slope [deg]')
    ax1.set_title('Elevation vs slopes for 10m resolution')
    ax1.legend()

def timeline(filtered_df):
    ####time bar plot
    dates = pd.DataFrame()
    dates["dates"] = pd.to_datetime(filtered_df['regDato'])
    dates["regStatus"]= filtered_df["regStatus"]
    yearly_counts = dates.groupby([dates['dates'].dt.year, 'regStatus']).size().unstack(fill_value=0)
    # Combine the counts for years before 2004 into an overflow bin
    mask = yearly_counts.index < 2004
    overflow_counts = pd.Series(yearly_counts[mask].sum(), index=['Before 2004'])
    yearly_counts = pd.concat([overflow_counts, yearly_counts[~mask]])
    # Reset the index of yearly_counts
    yearly_counts.reset_index(inplace=True)

    plt.figure(figsize=(10, 6))
    colors = {'Godkjent kvalitet A': 'tab:blue', 'Godkjent kvalitet B': 'tab:orange', 'Godkjent kvalitet C': 'tab:green' }
    yearly_counts.plot(kind='bar', stacked = True, edgecolor='black',colormap=plt.cm.tab20,)
    plt.xlabel('Year', fontsize = 20)
    plt.ylabel('Number of Events', fontsize =20)
    plt.title('Yearly Events Histogram', fontsize= 20)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def sink_stats(filtered_df):
    # Count the occurrences of 1 and 0 in the 'sinks' column
    sink_counts50 = filtered_df['sinks_50'].value_counts()
    sink_counts10 = filtered_df['sinks_50'].value_counts()
    min_sink_counts50 = filtered_df['min_sinks_50'].value_counts()
    min_sink_counts10 = filtered_df['min_sinks_50'].value_counts()
    print(sink_counts50, sink_counts10, min_sink_counts10, min_sink_counts50)
    # Create a bar plot


df1 = pd.read_pickle("/home/chris/OneDrive/Impetus/Slushflow_db/Ele_sink_uphill.pickle")
grades = ['Godkjent kvalitet A', 'Godkjent kvalitet B' , "Godkjent kvalitet C"]
filtered_df = df1[df1['regStatus'].isin(grades)]

# Use value_counts() to get unique strings and their frequencies
#reg_status_counts = df1['regStatus'].value_counts()
