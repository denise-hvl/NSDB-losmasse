from osgeo import gdal
import numpy as np
import lookup_on_raster
import os


path_dem_folder = r"/home/chris/OneDrive/dem50/"
dem_list = lookup_on_raster.dem_folder_lists(path_dem_folder, "/**/*_50m_33.tif")

for dem_path in dem_list:
    if os.path.isdir(dem_path):
        print("path continue ",dem_path)
        continue
    path = os.path.dirname(dem_path)  # this is the path name
    file = os.path.basename(dem_path)  # this is the file name
    if "sinks" in path:
        print("sinks continue", dem_path)
        continue
    elif "uphill" in path:
        print("uphill continue", dem_path)
        continue
    elif "slopes" in path:
        continue
    print(file)
    # Open the DEM raster
    dem_dataset = gdal.Open(dem_path)

    # Read the DEM data into a numpy array
    dem_array = dem_dataset.ReadAsArray()

    # Calculate the slope in degrees using numpy gradient function
    slope_x, slope_y = np.gradient(dem_array)
    slope_radians = np.arctan(np.sqrt(slope_x**2 + slope_y**2))
    slope_degrees = np.degrees(slope_radians)

    # Create the output raster
    driver = gdal.GetDriverByName('GTiff')
    output_path = path + r"/slopes/slopes" + file
    output_dataset = driver.Create(output_path, dem_dataset.RasterXSize, dem_dataset.RasterYSize, 1, gdal.GDT_Float32)

    # Set the geotransform and projection from the original DEM
    output_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
    output_dataset.SetProjection(dem_dataset.GetProjection())

    # Write the slope data into the output raster band
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(slope_degrees)

    # Close the datasets
    output_dataset = None
    dem_dataset = None
