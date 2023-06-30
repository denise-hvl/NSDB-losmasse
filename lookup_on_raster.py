import gdal
import geopandas as gpd
from datetime import datetime
import pandas as pd
import os

def lookup_raster(dem_raster_path,release_points_path):
    # Open the DEM raster using GDAL
    dem_dataset = gdal.Open(dem_raster_path)
    dem_band = dem_dataset.GetRasterBand(1)

    # Open the avalanche release point shapefile using GDAL
    driver = ogr.GetDriverByName('ESRI Shapefile')
    release_points_dataset = driver.Open(release_points_path, 0)
    release_points_layer = release_points_dataset.GetLayer()

    # Iterate over each release point
    for feature in release_points_layer:
        point_geometry = feature.GetGeometryRef()
        x = point_geometry.GetX()
        y = point_geometry.GetY()

        # Convert the release point coordinates to pixel coordinates
        gt = dem_dataset.GetGeoTransform()
        px = int((x - gt[0]) / gt[1])
        py = int((y - gt[3]) / gt[5])

        # Read the elevation value from the DEM raster
        elevation = dem_band.ReadAsArray(px, py, 1, 1)[0, 0]

        # Print the elevation value
        print('Avalanche release point: ({}, {}), Elevation: {}'.format(x, y, elevation))

    # Close the datasets
    dem_dataset = None
    release_points_dataset = None


def moasaic(dem_folder):
    # Output mosaic file path
    output_mosaic_path = 'path_to_output_mosaic.tif'

    # Get a list of subfolders in the main DEM folder
    subfolders = next(os.walk(dem_folder))[1]

    # List to store the individual DEM datasets
    dem_datasets = []

    # Iterate over the subfolders and open each DEM file
    for subfolder in subfolders:
        subfolder_path = os.path.join(dem_folder, subfolder)
        dem_file = next((f for f in os.listdir(subfolder_path) if f.endswith('.tif')), None)

    if dem_file:
        dem_path = os.path.join(subfolder_path, dem_file)
        dem_dataset = gdal.Open(dem_path)

        if dem_dataset:
            dem_datasets.append(dem_dataset)
        else:
            print(f'Failed to open DEM file: {dem_path}')

# Check if any DEM datasets were found
if len(dem_datasets) == 0:
    print('No DEM files found in the subfolders.')
    exit()

# Get the first DEM dataset to use as a reference
first_dem_dataset = dem_datasets[0]

# Get the geospatial information from the reference dataset
geotransform = first_dem_dataset.GetGeoTransform()
projection = first_dem_dataset.GetProjection()
cols = first_dem_dataset.RasterXSize
rows = first_dem_dataset.RasterYSize
band_count = first_dem_dataset.RasterCount
data_type = first_dem_dataset.GetRasterBand(1).DataType

# Create the output mosaic dataset
driver = gdal.GetDriverByName('GTiff')
mosaic_dataset = driver.Create(output_mosaic_path, cols, rows, band_count, data_type)
mosaic_dataset.SetGeoTransform(geotransform)
mosaic_dataset.SetProjection(projection)

# Iterate over the DEM datasets and merge them into the mosaic dataset
for i, dem_dataset in enumerate(dem_datasets):
    for band_index in range(1, band_count + 1):
        dem_band = dem_dataset.GetRasterBand(band_index)
        mosaic_band = mosaic_dataset.GetRasterBand(band_index)

        data = dem_band.ReadAsArray()
        mosaic_band.WriteArray(data, 0, 0)

        dem_band = None
        mosaic_band = None

    print(f'DEM {i+1} merged into the mosaic.')

# Close the mosaic dataset
mosaic_dataset = None

print('Mosaic creation completed.')


path_release = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\Slushflow_db\NVE_60751B14_1683888916789_12228\NVEData\Skred_Skredhendelse"
path_dem_folder = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\North_dem\Nedlastingspakke"
release_points_path = path_release + '\subset_release.shp'
#subset_poly = gpd.read_file(path +'\subset_poly.shp')

# Path to your DEM raster file
print("I made it here")

moasaic(path_dem_folder)
#lookup_raster(dem_raster_path,release_points_path)