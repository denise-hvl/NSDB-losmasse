from osgeo import gdal, ogr
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

def raster_extent(raster_path):
    raster_dataset = gdal.Open(raster_path)
    raster_extent = [
        raster_dataset.GetGeoTransform()[0],
        raster_dataset.GetGeoTransform()[0] + raster_dataset.RasterXSize * raster_dataset.GetGeoTransform()[1],
        raster_dataset.GetGeoTransform()[3] + raster_dataset.RasterYSize * raster_dataset.GetGeoTransform()[5],
        raster_dataset.GetGeoTransform()[3]
    ]
    return raster_extent

def points_in_tile(points, raster_extent):
    points_within_extent = points.cx[raster_extent[0]:raster_extent[1], raster_extent[3]:raster_extent[2]]
    return points_within_extent


if __name__ == "__main__":
    path_release = r"/home/chris/Documents/Slushflow_db/"
    path_dem_folder = r"/home/chris/Documents/North_dem/Nedlastingspakke"
    release_points_path = path_release + '/slushflows.shp'
    points = gpd.read_file(release_points_path)
    #subset_poly = gpd.read_file(path +'\subset_poly.shp')
    raster_extent = raster_extent(path_dem_folder + "/7504_3_10m_z33.tif")
    extent_points = points_in_tile(points, raster_extent)
    print(extent_points)


    #lookup_raster(dem_raster_path,release_points_path)