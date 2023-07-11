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
    max_uphill_dict = {}
    min_sink_dict = {}
    for raster_tile in raster_list:
        if os.path.isdir(raster_tile):
            continue
        path = os.path.dirname(raster_tile) # this is the path name
        file = os.path.basename(raster_tile) #this is the file name
        if "sinks" in file:
            continue
        elif "uphill" in file:
            continue
        print(path, file)
        raster_extent = raster_extents(raster_tile)
        extent_points = points_in_tile(points, raster_extent)

        raster_dataset = gdal.Open(raster_tile) # this opens the raster file
        sinks_dataset = gdal.Open(path + "/sinks/sinks" + file)
        uphill_dataset = gdal.Open(path + "/uphill/uphill" + file )
        # Get the height and width of the raster
        raster_height = raster_dataset.RasterYSize
        raster_width = raster_dataset.RasterXSize

        for idx, point in extent_points.iterrows():
            # Get the point's coordinates
            point_x = point.geometry.x
            point_y = point.geometry.y

            # Get the pixel coordinates in the DEM raster corresponding to the CENTER point
            #row, col = raster_dataset.index(point_x, point_y)

            ## Looking at neighbor cells
            geotransform = raster_dataset.GetGeoTransform()
            col = int((point_x - geotransform[0]) / geotransform[1])
            row = int((point_y - geotransform[3]) / geotransform[5])

            band_ele = raster_dataset.GetRasterBand(1)
            attribute = band_ele.ReadAsArray(col, row, 1, 1)[0][0]

            band_sink = sinks_dataset.GetRasterBand(1)
            attribute1 = band_sink.ReadAsArray(col, row, 1, 1)[0][0]

            band_uphill = uphill_dataset.GetRasterBand(1)
            attribute2 = band_uphill.ReadAsArray(col, row, 1, 1)[0][0]

            sink_values = []
            uphill_values = []
            for i in range(max(row - 1, 0), min(row + 2, raster_height)):
                for j in range(max(col - 1, 0), min(col + 2, raster_width)):

                    # sinks
                    sink_value = band_sink.ReadAsArray(j, i, 1, 1)[0][0]
                    sink_values.append(sink_value)


                    # uphill potential
                    uphill_value = band_uphill.ReadAsArray(j, i, 1, 1)[0][0]
                    uphill_values.append(uphill_value)

            min_sink = min(sink_values)
            min_sink_dict[point["skredID"]] = min_sink
            max_uphill = max(uphill_values)
            max_uphill_dict[point["skredID"]] = max_uphill


            # Get the elevation value at the pixel coordinates
            #attribute = raster_dataset.read(1)[row, col]
            attribute_dict[point["skredID"]]= attribute
            #attribute1 = sinks_dataset.read(1)[row1, col1]
            attribute1_dict[point["skredID"]]= attribute1
            #attribute2 = uphill_dataset.read(1)[row2, col2]
            attribute2_dict[point["skredID"]]= attribute2
    return attribute_dict, attribute1_dict, attribute2_dict, min_sink_dict, max_uphill_dict


if __name__ == "__main__":
    path_release = r"/home/chris/Documents/Slushflow_db/"
    path_dem_folder = r"//home/chris/OneDrive/DEM/"
    release_points_path = path_release + '/slushflows.shp'
    points = gpd.read_file(release_points_path)
    #subset_poly = gpd.read_file(path +'\subset_poly.shp')
    dem_list = dem_folder_lists(path_dem_folder, "/**/*_10m_*.tif" ) # this is a list of dem path names
    elevation_dict, sinks_dict, uphill_dict, min_sink_dict, max_uphill_dict = lookup_on_raster(dem_list,points)
    points["elevation"] = points["skredID"].map(elevation_dict)
    points["uphill potential"] = points["skredID"].map(uphill_dict)
    points["sinks"] = points["skredID"].map(sinks_dict)
    points["min_sinks"] = points["skredID"].map(min_sink_dict)
    points["max_uphill"] = points["skredID"].map(max_uphill_dict)
    points.to_pickle(r"/home/chris/OneDrive/Impetus/Slushflow_db/Ele_sink_uphill.pickle")
    print("done")

    #lookup_raster(dem_raster_path,release_points_path)