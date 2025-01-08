import geopandas as gpd
import os
import pandas as pd
import json
from topojson import Topology
from shapely.geometry import Polygon, LineString
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 250)

year = '2025'


filepath = r''
filename = 'postaldistricts.shp'

def remove_z(geom):
    if geom.has_z:
        if geom.geom_type == 'Polygon':
            return Polygon([(x, y) for x, y, *_ in geom.exterior.coords])
        elif geom.geom_type == 'LineString':
            return LineString([(x, y) for x, y, *_ in geom.coords])
        else:
            return geom  # Retain as-is for other geometry types
    return geom

gdf = gpd.read_file(os.path.join(filepath, filename))  # Read your shapefile (or other data source)
gdf = gdf.to_crs("EPSG:4326")
print(gdf.head())

# Apply the function to the GeoDataFrame's geometry column
gdf['geometry'] = gdf['geometry'].apply(remove_z)
# gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.0001, preserve_topology=True) # lowres
gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.00001, preserve_topology=True) # highres

# Step 2: Convert the GeoDataFrame to a GeoJSON dictionary
if year == '2024':
    geojson_dict = json.loads(gdf[['nouveau_PO', 'geometry']].to_json())
elif year == '2025':
    geojson_dict = json.loads(gdf[['new_po', 'geometry']].to_json())

# Step 3: Use Topology to convert GeoJSON to TopoJSON
topo = Topology(geojson_dict, prequantize=False)
topojson_data = topo.to_dict()  # Convert Topology object to dictionary

with open("postaldistricts_highres_2025.json", "w") as f:
    json.dump(topo.to_dict(), f, indent=2)

''