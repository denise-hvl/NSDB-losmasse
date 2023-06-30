# make a plot of the number of envents with a quality tag.
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime
import pandas as pd

def quality_points(data):
    counts = data['regStatus'].value_counts()
    total_count = counts.sum()
    # create a pie chart of the counts
    counts.plot(kind='pie', autopct='%1.1f%%')

    for i, v in enumerate(counts):
        plt.gca().text(0, 0, str(v), ha='center', va='center')

    plt.title('Point data total Count: {}'.format(total_count))
    plt.show()
    # display the pie chart


def timeline(subset_release):
    #subset_release["regDato"] = pd.to_datetime(subset_release["regDato"])
    subset_release['regDato'] = pd.to_datetime(subset_release['regDato'])
    counts = subset_release.groupby(pd.Grouper(key='regDato', freq='M')).count()
    #subset_release['timestamp'] = subset_release['regDato'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').timestamp())
    counts.plot(kind='bar')
    plt.xticks(rotation=45)
   #plt.gca().xaxis.set_major_formatter(plt.FixedFormatter(subset_release['regDato']))

def quality_poly(subset_release, subset_poly):
    subset_poly = subset_poly.merge(subset_release[['skredID', 'regStatus']], on='skredID')
    counts = subset_poly['regStatus_y'].value_counts()
    total_count = counts.sum()
    # create a pie chart of the counts
    counts.plot(kind='pie', autopct='%1.1f%%')

    for i, v in enumerate(counts):
        plt.gca().text(0, 0, str(v), ha='center', va='center')

    plt.title('Polygone data total Count: {}'.format(total_count))
    plt.show()

# read the subset release file
# this file is not really release but more of a quality checked layer with only polygon data
path = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\Slushflow_db\NVE_60751B14_1683888916789_12228\NVEData\Skred_Skredhendelse"
subset_release = gpd.read_file(path + '\subset_release.shp')
subset_poly = gpd.read_file(path +'\subset_poly.shp')

#run our plot functions
quality_points(subset_release)
timeline(subset_release)
#quality_poly(subset_release,subset_poly)
plt.show()
