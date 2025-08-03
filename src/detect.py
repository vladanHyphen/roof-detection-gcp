import argparse
import rasterio
from utils import dummy_model, polygons_from_mask, save_geojson

def main(args):
    # "Load" a model (placeholder logic)
    model = dummy_model

    # Load image (just for shape)
    with rasterio.open(args.input) as src:
        image = src.read([1, 2, 3])
        transform = src.transform
        crs = src.crs

    # Predict mask (dummy: blank mask)
    mask = model(image)

    # Convert mask to polygons
    polygons = polygons_from_mask(mask, transform)

    # Save polygons as GeoJSON
    save_geojson(polygons, args.output, crs)
    print(f"Detection results saved to {args.output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help="Input GeoTIFF image path")
    parser.add_argument('--output', type=str, required=True, help="Output GeoJSON path")
    args = parser.parse_args()
    main(args)
