def get_geojson_template():
    template = {
        "type": "FeatureCollection",
        "features": []
    }

    return template

def get_feature_template():
    template = {
        "type": "Feature",
        "geometry": {
            "type": "Point"
        },
        "properties": {}
    }

    return template
