# https://blog.haardiek.org/plotting-sentinel-5p-data.html
import os
import s5a
import glob


no2path = os.path.join(os.path.dirname(os.sys.path[0]),"data/NO2Files/")

print(no2path)

files = os.listdir(no2path)

data = s5a.load_ncfile(
    no2path + files[0]
)
dataraw = data
data = s5a.filter_by_quality(data)
data = s5a.point_to_h3(data, resolution=10)
data = s5a.aggregate_h3(data)
data = s5a.h3_to_point(data)

datafiltered = data
# print(data2.head())

import geopandas

geometry = geopandas.points_from_xy(data.longitude, data.latitude)
data = geopandas.GeoDataFrame(data, geometry=geometry, crs={'init' :'epsg:4326'})

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
worldplot = world.plot(figsize=(10, 5))

robinson_projection = '+a=6378137.0 +proj=robin +lon_0=0 +no_defs'
world = world.to_crs(robinson_projection)
data = data.to_crs(robinson_projection)

import matplotlib.pyplot as plt
# Define base of the plot.
fig, ax = plt.subplots(1, 1, figsize=(40, 40), dpi=100)
# Disable the axes
ax.set_axis_off()
# Plot the data
data.plot(
    column='value',  # Column defining the color
    cmap='rainbow',  # Colormap
    marker='H',  # marker layout. Here a Hexagon.
    markersize=1,
    ax=ax,  # Base
    vmax=0.0005,  # Used as max for normalize luminance data
)

print(type(data))
# Plot the boundary of the countries on top
worldplot = world.geometry.boundary.plot(color=None, edgecolor='black', ax=ax)

# worldplot.figure.savefig(os.path.join(os.sys.path[0],'books_read.png'))
