from shapely.geometry import Polygon
import geopandas as gpd
import numpy as np

def dummy_model(image):
    # Returns a blank mask (no roofs detected)
    return np.zeros((image.shape[1], image.shape[2]), dtype=np.uint8)

def polygons_from_mask(mask, transform):
    # Dummy: Returns empty list (no detections)
    # Replace with actual logic using e.g. skimage.measure.find_contours for real model output
    return []

def save_geojson(polygons, out_path, crs):
    gdf = gpd.GeoDataFrame(geometry=polygons, crs=crs)
    gdf.to_file(out_path, driver="GeoJSON")
