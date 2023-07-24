import matplotlib.pyplot as plt
import pickle
import geopandas as gpd
import numpy as np
import pandas as pd
import contextily as ctx
import seaborn as sns
from PIL import ImageColor

class Colors:
    def __init__(self):
        self.colora = "#003f5c"
        self.colorb = "#bc5090"
        self.colorc = "#ffa600"
        self.color10 = "#95E0E6"
        self.color50 = "#95E69C"
        self.color10N = "#9B95E6"

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

def Elevation_box_plot(filter_df):
    c = Colors()
    filter_df = filter_df.replace("Godkjent kvalitet","Quality",regex=True) #replace column name to english
    colory = [c.colora,c.colorb,c.colorc]
    # Set your custom color palette
    sns.set_palette(sns.color_palette(colory))
    sns.boxplot(x = "regStatus", y = "elevation_10", data = filter_df, order=["Quality A", "Quality B","Quality C"])
    plt.title('Elevation Box Plot', fontsize = 24)
    plt.xlabel('Quality Grade', fontsize = 20)
    plt.ylabel('Elevation [m]', fontsize = 20)
    grade_string = ["Quality A"," Quality B","Quality C"]
    #plt.set_xticklabels(grade_string)
    plt.suptitle('')  # Remove the default 'Boxplot grouped by...'
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    plt.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/elevation_box_plot.png")

def slopes_box_plot(filter_df):
    c = Colors()
    filter_df = filter_df.replace("Godkjent kvalitet", "Quality", regex=True)
    colory = [c.colora, c.colorb, c.colorc]
    # Set your custom color palette
    sns.set_palette(sns.color_palette(colory))
    sns.boxplot(x="regStatus", y="slopes_10", data=filter_df, order=["Quality A", "Quality B", "Quality C"])
    plt.title('Slopes Box Plot by Quality Grade', fontsize=24)
    plt.xlabel('Quality Grade', fontsize=20)
    plt.ylabel('Slopes', fontsize=20)
    plt.suptitle('')  # Remove the default 'Boxplot grouped by...'
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    plt.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/slopes_box_plot.png")

def up_hilll_hist(filtered_df):
    # uphill potential plot
    colors = Colors()
    fig, ax = plt.subplots()

    bin_edges = list(range(0, 100, 5)) + [np.inf]
    ax.hist([filtered_df['uphill potential_10'],filtered_df['max_uphill_50']], bins = bin_edges, color = [colors.color10, colors.color10N], label=["10m on point","Max from Neighbors "])
    # Add labels, title, and legend
    ax.set_xlabel('uphill potential (cells)', fontsize = 20)
    ax.set_ylabel('Frequency', fontsize = 20)
    ax.set_title('Uphill potential (A & B)' , fontsize = 24)
    ax.legend(fontsize = "16")
    plt.tight_layout()
    fig.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/uphill_hist.png")

def slopes_elevation(df1):
    colors = Colors()
    fig1, ax1 = plt.subplots()
    dfA = df1[df1['regStatus'] == 'Godkjent kvalitet A']
    dfB = df1[df1['regStatus'] == 'Godkjent kvalitet B']
    dfC = df1[df1['regStatus'] == 'Godkjent kvalitet C']

    ax1.scatter(dfA["elevation_10"], dfA["slopes_10"], color= colors.colora, label = "Quality A", zorder = 3)
    ax1.scatter(dfB["elevation_10"], dfB["slopes_10"], color = colors.colorb, label = "Quality B", zorder = 2 )
    ax1.scatter(dfC["elevation_10"], dfC["slopes_10"], color = colors.colorc, label="Quality C", zorder=1)
    ax1.set_xlabel('Elevation [m]', fontsize = 20)
    ax1.set_ylabel('Slope [deg]', fontsize = 20)
    ax1.set_title('Elevation vs slopes (10 m DEM)', fontsize = 24)
    ax1.legend(fontsize = "16")
    plt.tight_layout()
    fig1.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/uphill.png")

def timeline(filtered_df):
    ####time bar plot
    c = Colors()
    dates = pd.DataFrame()
    dates["dates"] = pd.to_datetime(filtered_df['regDato'])
    dates["regStatus"]= filtered_df["regStatus"]
    yearly_counts = dates.groupby([dates['dates'].dt.year, 'regStatus']).size().unstack(fill_value=0)
    # Combine the counts for years before 2004 into an overflow bin
    before2004 = yearly_counts[yearly_counts.index <2004]['Godkjent kvalitet C'].sum()
    mask = yearly_counts.index < 2004
    yearly_counts.index = yearly_counts.index.astype(int).astype(str) # convert years in index to a string
    new_row =pd.DataFrame({"Godkjent kvalitet A": 0,"Godkjent kvalitet B": 0,"Godkjent kvalitet C": before2004}, index =["1951 - 2004"])
    yearly_counts = pd.concat([new_row,yearly_counts[~mask]])

    plt.figure(figsize=(10, 6))
    yearly_counts = yearly_counts[yearly_counts.columns[::-1]]
    ax = yearly_counts.plot(kind='bar', stacked = True,edgecolor='black',color=[c.colorc,c.colorb,c.colora],)
    plt.xlabel('Year', fontsize = 20)
    plt.ylabel('Number of Events', fontsize =20)
    plt.title('Yearly Events Histogram', fontsize= 20)
    plt.xticks(rotation=90)
    handles, labels = ax.get_legend_handles_labels()
    labels = ["Quality A","Quality B","Quality C"]
    ax.legend(reversed(handles), labels, fontsize = 16)

    plt.tight_layout()
    plt.savefig(r"/home/chris/OneDrive/talks/ISSW2023/figs/timeline.png")


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
#slopes_box_plot(filtered_df)
#Elevation_box_plot(filtered_df)
#timeline(filtered_df) # done
#up_hilll_hist(filtered_df) # done
#slopes_elevation(df1) # done
plt.show()
# Use value_counts() to get unique strings and their frequencies
#reg_status_counts = df1['regStatus'].value_counts()
