from osgeo import gdal
import numpy as np
import lookup_on_raster
import os


path_dem_folder = r"/home/chris/OneDrive/DEM/"
dem_list = lookup_on_raster.dem_folder_lists(path_dem_folder, "/**/*_10m_z33.tif")

for dem_path in dem_list:
    # Open the DEM raster
    path = os.path.dirname(dem_path) # here is the path name
    file = os.path.basename(dem_path) #this is the file name
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
