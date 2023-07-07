"""
this code will open a dem and then delineate the drainage catchment. There must be a sink fill routine run before that.
A goal for after that is to pick a point and then describe how much catchment is behind that point.
"""
import pandas
import rasterio
import pysheds
import os
import numpy as np
import matplotlib as plt
import lookup_on_raster
from pysheds.grid import Grid


path_dem_folder = r"/home/chris/Documents/North_dem/Nedlastingspakke"
dem_list = lookup_on_raster.dem_folder_lists(path_dem_folder, "/**/*_10m_z33.tif")


for dem_path in dem_list:
    print(dem_path)
    path = os.path.dirname(dem_path)
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)
    filled_dem = grid.fill_depressions(dem)
    sinks = grid.detect_depressions(dem) # these are the cells with not outflow where pooling could happen.
    sinks = grid.detect_pits(sinks)
    sinks = grid.detect_flats(sinks)
    inflated_dem = grid.resolve_flats(filled_dem)
    dirmap = (1, 2, 3, 4, 5, 6, 7, 8)
    flowdir = grid.flowdir(inflated_dem, dirmap = dirmap) # i think this is 8 direction flow or steepest decent.
    uphill_potential = grid.accumulation(flowdir) # accumulation of the flow direction shows how much flux in each cell this should be the output for slushflows.

    with rasterio.open(dem_path) as dem_src:
        dem_meta = dem_src.meta

        with rasterio.open(path + r"/sinks.tif", "w" , **dem_meta) as sinks_dst:
            sinks_dst.write(sinks.astype(rasterio.uint8),1) # uint8 0-255
        with rasterio.open(path + r"/uphill_potential.tif", "w", **dem_meta) as uphill_potential_dst:
            uphill_potential_dst.write(uphill_potential.astype(rasterio.uint16), 1) # uint16 is 0-65535



"""
    #### plot routine
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors

    fig, ax = plt.subplots(figsize=(8,6))
    fig.patch.set_alpha(0)
    plt.grid('on', zorder=0)
    im = ax.imshow(sinks, extent=grid.extent, zorder=2,
                   cmap='cubehelix',
                   norm=colors.LogNorm(1, sinks.max()),
                   interpolation='bilinear')
    plt.colorbar(im, ax=ax, label='Upstream Cells')
    plt.title('Flow Accumulation', size=14)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.tight_layout()
    plt.show()
"""