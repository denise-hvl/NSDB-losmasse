from osgeo import gdal, ogr
import geopandas as gpd
import glob
import rasterio
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

def raster_extents(raster_path):
    raster_dataset = gdal.Open(raster_path)
    raster_extent = [
        raster_dataset.GetGeoTransform()[0],
        raster_dataset.GetGeoTransform()[0] + raster_dataset.RasterXSize * raster_dataset.GetGeoTransform()[1],
        raster_dataset.GetGeoTransform()[3] + raster_dataset.RasterYSize * raster_dataset.GetGeoTransform()[5],
        raster_dataset.GetGeoTransform()[3]
    ]
    return raster_extent

def points_in_tile(points, raster_extent):
    """
    This function picks out the points that lay within one DEM tile.
    :param points: a set of GIS points
    :param raster_extent: outline of the rasters extent
    :return: List of points that lay within the extent of the raster
    """
    points_within_extent = points.cx[raster_extent[0]:raster_extent[1], raster_extent[3]:raster_extent[2]]
    return points_within_extent


def dem_folder_lists(path_dem_folder, string_check):
    """
    Makes a list of DEM files.
    :param path_dem_folder:
    :return: list of files containing the string
    """
    path = path_dem_folder + string_check # this is looking for _10m_ to identify the dems in all the sub folders
    dem_list = glob.glob(path, recursive= True) # glob brings in * use like in linux, recursive looks in subfolders
    return dem_list

def lookup_on_raster(raster_list, points): # loops over list of raster files and picks out values for each point
    attribute_dict = {}
    attribute1_dict = {}
    attribute2_dict = {}
    for raster_tile in raster_list:
        path = os.path.dirname(raster_tile)
        raster_extent = raster_extents(raster_tile)
        extent_points = points_in_tile(points, raster_extent)

        raster_dataset = rasterio.open(raster_tile) # this opens the raster file
        sinks_dataset = rasterio.open(path + "/sinks.tif")
        uphill_dataset = rasterio.open(path + "/uphill_potential.tif")
        for idx, point in extent_points.iterrows():
            # Get the point's coordinates
            point_x = point.geometry.x
            point_y = point.geometry.y

            # Get the pixel coordinates in the DEM raster corresponding to the point
            row, col = raster_dataset.index(point_x, point_y)
            row1, col1 = sinks_dataset.index(point_x, point_y)
            row2, col2 = uphill_dataset.index(point_x, point_y)

            # Get the elevation value at the pixel coordinates
            attribute = raster_dataset.read(1)[row, col]
            attribute_dict[point["skredID"]]= attribute
            attribute1 = sinks_dataset.read(1)[row1, col1]
            attribute1_dict[point["skredID"]]= attribute1
            attribute2 = uphill_dataset.read(1)[row2, col2]
            attribute2_dict[point["skredID"]]= attribute2
    return attribute_dict, attribute1_dict, attribute2_dict


if __name__ == "__main__":
    path_release = r"/home/chris/Documents/Slushflow_db/"
    path_dem_folder = r"/home/chris/Documents/North_dem/Nedlastingspakke"
    release_points_path = path_release + '/slushflows.shp'
    points = gpd.read_file(release_points_path)
    #subset_poly = gpd.read_file(path +'\subset_poly.shp')
    dem_list = dem_folder_lists(path_dem_folder, "/**/*_10m_*.tif" ) # this is a list of dem path names
    elevation_dict, sinks_dict, uphill_dict = lookup_on_raster(dem_list,points)
    points["elevation"] = points["skredID"].map(elevation_dict)
    points["uphill potential"] = points["skredID"].map(uphill_dict)
    points["sinks"] = points["skredID"].map(sinks_dict)
    points.to_pickle(r"/home/chris/Documents/Slushflow_db/Ele_sink_uphill.pickle")
    print("done")
    # todo make sink (true/false) uphill potential based on look_up_raster
    # todo export the dataframe in a pickle

    #lookup_raster(dem_raster_path,release_points_path)