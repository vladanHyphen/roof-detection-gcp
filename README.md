# Roof Detection Tool

This project detects building roofs from high-resolution aerial/satellite imagery using deep learning.
Results are exported as georeferenced polygons for GIS integration.

## Features

- Segmentation of roofs from imagery.
- Export to GeoJSON, Shapefile, or CSV.
- Designed for Google Cloud Platform (GCP) deployment.
- Version controlled with GitHub.

## Quick Start

1. Clone the repo:
    ```
    git clone https://github.com/yourusername/roof-detection-gcp.git
    cd roof-detection-gcp
    ```

2. Install requirements:
    ```
    pip install -r requirements.txt
    ```

3. Run detection:
    ```
    python src/detect.py --input data/sample_image.tif --output results.geojson
    ```

4. For GCP deployment, see [`scripts/deploy_gcp.sh`](scripts/deploy_gcp.sh).

## GCP

This tool can be deployed as a batch job, REST API, or scheduled workflow on Google Cloud. See [GCP Deployment](#gcp-deployment) in this README.

## License

MIT
