from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import os

api = SentinelAPI('', '', 'https://s5phub.copernicus.eu/dhus/')
# http://geojson.io/

print(os.sys.path[0])
print(os.path.join(os.sys.path[0],'NO2Files'))
# quit()
footprint = geojson_to_wkt(read_geojson(os.path.join(os.sys.path[0],'search_polygon.geojson')))
products = api.query(footprint,
                     date = ('20200315', '20200322'),
                     producttype='L2__NO2___',
                     area_relation = 'Contains')
# prod = products['3ddb44b3-c92c-4537-bd7a-2fb1539a2027']
print(products)
api.download_all(products, directory_path=os.path.join(os.sys.path[0],'NO2Files'))
# df = api.to_dataframe(products)
# print(df)
# print(os.path.join(os.sys.path[0],'search_polygon.geojson'))

# import numpy as np
# import pandas as pd
# from netCDF4 import Dataset
