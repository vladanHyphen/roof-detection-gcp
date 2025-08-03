from flask import Flask, request, jsonify, send_file, send_from_directory, Response
from io import BytesIO
import pandas as pd
import json
import math
import uuid

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/detect-buildings', methods=['POST'])
def detect_buildings():
    data = request.get_json()
    bbox = data.get('bbox')  # [minLat, minLon, maxLat, maxLon]

    if not bbox or len(bbox) != 4:
        return jsonify({"error": "Invalid bounding box"}), 400

    min_lat, min_lon, max_lat, max_lon = bbox

    # Target size ~111 meters (approx 0.001 degrees latitude)
    target_meters = 111  # ~111 meters per rectangle side

    # Latitude step fixed (degrees)
    target_lat_size = 0.001  # approx 111m latitude

    # Calculate longitude degree length at bbox center latitude
    lat_center = (min_lat + max_lat) / 2
    meters_per_degree_lon = 111320 * math.cos(math.radians(lat_center))
    target_lon_size = target_meters / meters_per_degree_lon  # degrees longitude

    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon

    rows = max(1, math.ceil(lat_range / target_lat_size))
    cols = max(1, math.ceil(lon_range / target_lon_size))

    lat_step = lat_range / rows
    lon_step = lon_range / cols

    features = []
    for i in range(rows):
        for j in range(cols):
            rect_min_lat = min_lat + i * lat_step
            rect_max_lat = rect_min_lat + lat_step
            rect_min_lon = min_lon + j * lon_step
            rect_max_lon = rect_min_lon + lon_step

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [rect_min_lon, rect_min_lat],
                        [rect_max_lon, rect_min_lat],
                        [rect_max_lon, rect_max_lat],
                        [rect_min_lon, rect_max_lat],
                        [rect_min_lon, rect_min_lat],
                    ]]
                },
                "properties": {"label": f"Building {i*cols + j + 1}"}
            })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return jsonify({"geojson": geojson})

@app.route('/export-excel', methods=['POST'])
def export_excel():
    data = request.get_json()
    geojson = data.get('geojson')

    rows = []
    for feature in geojson.get('features', []):
        coords = feature['geometry']['coordinates'][0]
        label = feature['properties'].get('label', '')

        # Generate unique IDs for this building polygon
        tx_global_id = str(uuid.uuid4()).upper()
        geopoint_guid = str(uuid.uuid4()).upper()

        # Example fixed values, modify as needed
        mrn_id_uniqueid = "986200150_00039_1"
        psu_no_m = "986200150"
        ea_code = "986200150"
        mrn = "986200150_00039"
        du_number = "39"
        record_no = "1"
        feature_category = "2"

        for idx, (lon, lat) in enumerate(coords):
            rows.append({
                'TxGlobalID (structure Guid)': tx_global_id,
                'GEOPOINT_GUID': geopoint_guid,
                'MRN_ID_UNIQUEID': mrn_id_uniqueid,
                'PSU_NO_M': psu_no_m,
                'EA_CODE': ea_code,
                'MRN_ID': mrn,
                'MRN': mrn,
                'DU NUMBER': du_number,
                'RECORD NO': record_no,
                'FEATURE CATEGORY': feature_category,
                'Building Label': label,
                'Vertex Index': idx + 1,
                'Latitude': lat,
                'Longitude': lon
            })

    df = pd.DataFrame(rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Buildings')

    output.seek(0)
    return send_file(
    output,
    as_attachment=True,
    download_name='detected_buildings.xlsx',
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    conditional=False
)

@app.route('/export-geojson', methods=['POST'])
def export_geojson():
    data = request.get_json()
    geojson = data.get('geojson')
    if not geojson:
        return jsonify({"error": "No GeoJSON provided"}), 400

    geojson_str = json.dumps(geojson)

    return Response(
        geojson_str,
        mimetype='application/geo+json',
        headers={
            'Content-Disposition': 'attachment;filename=detected_buildings.geojson'
        }
    )

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

