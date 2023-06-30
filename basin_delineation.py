"""
this code will open a dem and then delineate the drainage catchment. There must be a sink fill routine run before that.
A goal for after that is to pick a point and then describe how much catchment is behind that point.
"""
import pandas
import rasterio
import pysheds
import numpy as np
import matplotlib as plt
from pysheds.grid import Grid
#dem_file = rasterio.open(r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\North_dem\Nedlastingspakke\Basisdata_7606-2_Celle_25833_DTM10UTM33_TIFF\7606_2_10m_z33.tif")
path = r"C:\Users\cda055\OneDrive - UiT Office 365\Impetus\North_dem\Nedlastingspakke\Basisdata_7605-1_Celle_25833_DTM10UTM33_TIFF"
grid = Grid.from_raster(path + r"\7605_1_10m_z33.tif")
dem = grid.read_raster(path + r"\7605_1_10m_z33.tif")
filled_dem = grid.fill_depressions(dem)
sinks = grid.detect_depressions(dem) # these are the cells with not outflow where pooling could happen.
sinks = grid.detect_pits(sinks)
sinks = grid.detect_flats(sinks)
inflated_dem = grid.resolve_flats(filled_dem)
dirmap = (1, 2, 3, 4, 5, 6, 7, 8)
flowdir = grid.flowdir(inflated_dem, dirmap = dirmap) # i think this is 8 direction flow or steepest decent.
uphill_potential = grid.accumulation(flowdir) # accumulation of the flow direction shows how much flux in each cell this should be the output for slushflows.

with rasterio.open(path + r"\7605_1_10m_z33.tif") as dem_src:
    dem_meta = dem_src.meta

    with rasterio.open(path + r"\sinks.tif", "w" , **dem_meta) as sinks_dst:
        sinks_dst.write(sinks.astype(rasterio.uint8),1) # uint8 0-255
    with rasterio.open(path + r"\uphill_potential.tif", "w", **dem_meta) as uphill_potential_dst:
            uphill_potential_dst.write(uphill_potential.astype(rasterio.uint16), 1) # uint16 is 0-65535
"""
import matplotlib.pyplot as plt
import matplotlib.colors as colors

fig, ax = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(0)
plt.grid('on', zorder=0)
im = ax.imshow(acc, extent=grid.extent, zorder=2,
               cmap='cubehelix',
               norm=colors.LogNorm(1, acc.max()),
               interpolation='bilinear')
plt.colorbar(im, ax=ax, label='Upstream Cells')
plt.title('Flow Accumulation', size=14)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()
"""