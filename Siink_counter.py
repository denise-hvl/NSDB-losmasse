from osgeo import gdal
import numpy as np
import lookup_on_raster
import rasterio
import os




def calculate_terrain_percentage(raster_file):
    with rasterio.open(raster_file) as src:
        # Read the raster data as a NumPy array
        data = src.read(1)

        # Count the number of 1 values in the raster
        count_ones = (data == 1).sum()

        # Calculate the total number of pixels in the raster
        total_pixels = data.size

        # Calculate the percentage of 1 values
        percentage_ones = (count_ones / total_pixels) * 100

        return percentage_ones

    # Replace 'sinks.tif' with the path to your actual raster file



path_dem_folder = r"/home/chris/OneDrive/DEM/sinks"
dem_list = lookup_on_raster.dem_folder_lists(path_dem_folder, "/**/sinks*_10m_z33.tif")
percent_list = []
for dem_path in dem_list:
    if os.path.isdir(dem_path):
        print("path continue ",dem_path)
        continue
    path = os.path.dirname(dem_path)  # this is the path name
    file = os.path.basename(dem_path)  # this is the file name

    if "uphill" in path:
        print("uphill continue", dem_path)
        continue
    elif "slopes" in path:
        continue
        #print(file)
    percentage_ones = calculate_terrain_percentage(dem_path)
    percent_list.append(percentage_ones)
    print(f"The percentage of terrain with 1 values is: {percentage_ones:.2f}%", file)

print("total average ",sum(percent_list)/len(percent_list))