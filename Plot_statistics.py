# make a plot of the number of envents with a quality tag.
import matplotlib.pyplot as plt
import geopandas as gpd

# read the subset release file
# this file is not really release but more of a quality checked layer with only polygon data
path = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\Slushflow_db\NVE_60751B14_1683888916789_12228\NVEData\Skred_Skredhendelse"
subset_release = gpd.read_file(path + '\subset_release.shp')

counts = subset_release['regStatus'].value_counts()
total_count = counts.sum()
# create a pie chart of the counts
counts.plot(kind='pie', autopct='%1.1f%%')

for i, v in enumerate(counts):
    plt.gca().text(0, 0, str(v), ha='center', va='center')

plt.title('Total Count: {}'.format(total_count))
# display the pie chart
plt.show()
