import matplotlib.pyplot as plt
import pickle
import geopandas
import numpy as np
import pandas as pd

df1 = pd.read_pickle("/home/chris/OneDrive/Impetus/Slushflow_db/Ele_sink_uphill.pickle")
df = df1[df1['regStatus'].isin(['Godkjent kvalitet A', 'Godkjent kvalitet B', "godkjent kvalitet C"])]
#df = df1[df1['regStatus'] == 'Godkjent kvalitet A']
column_names = ['elevation', 'uphill potential', 'sinks']
num_plots = len(column_names)
fig, axs = plt.subplots(num_plots)

for i, column_name in enumerate(column_names):
    if column_name == "elevation":
        bin_size = [0, 25, 50, 100, 200, 300, 400, 500, 750, 1000, 2000, np.inf]
        bin_size = [i for i in range(0, 2001, 25)]
    elif column_name == "uphill potential":
        bin_size = [5, 10,20,40,80,160,320,640,1280]
    elif column_name == "sinks":
        bin_size = [-1,0,1]
    axs[i].hist(df[column_name], bins = bin_size)
    axs[i].set_xlabel(column_name)
    axs[i].set_ylabel('Frequency')
    axs[i].set_title('Histogram of {}'.format(column_name))


plt.tight_layout()
plt.show()



