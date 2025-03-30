from flask import Flask, render_template, request, jsonify
import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from soil import SoilData
from folium.plugins import FastMarkerCluster
from models import CropModel, WeatherModel
from weather import Weather

app = Flask(__name__)

world = gpd.read_file("resources\\ne_10m_admin_0_countries.shp")

def get_countries_bulk(points):
    gdf_points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in points], crs=world.crs)
    joined = gpd.sjoin(gdf_points, world, how="left", predicate="within")
    return joined["NAME"].fillna("Unknown").tolist()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            lat = float(request.form["lat"])
            lng = float(request.form["lng"])
            crop_date = request.form["cropDate"]
            date_obj = pd.to_datetime(crop_date)
            day, month, year = date_obj.day, date_obj.month, date_obj.year

            soil_data = SoilData()
            N, P, K, pH = soil_data.get_data(lat, lng)

            weather_inst = Weather(lat, lng)
            weather_model = WeatherModel(weather_inst.data)
            weather_model.fit()
            temp_pred, rain_pred = weather_model.predict(day, month, year)

            crop_model = CropModel()
            crop_model.fit()
            input_features = pd.DataFrame({
                "N": [N],
                "P": [P],
                "K": [K],
                "pH": [pH],
                "temperature": [temp_pred],
                "rainfall": [rain_pred]
            })
            for col in crop_model.feature_names:
                if col not in input_features.columns:
                    input_features[col] = 0
            input_features = input_features[crop_model.feature_names]
            recommendation = crop_model.predict(input_features)
            return jsonify({"message": f"Recommended crop: {recommendation.capitalize()}"})
        except Exception as e:
            return jsonify({"message": f"Error: {e}"}), 400

    lat_series, lon_series = SoilData().get_points()
    points = list(zip(lat_series.values, lon_series.values))
    country_names = get_countries_bulk(points)

    # Create marker data with four elements: lat, lng, country, and popup HTML text.
    marker_data = [
        [
            pt[0],
            pt[1],
            country,
            f"Latitude: {pt[0]}<br>Longitude: {pt[1]}<br>Country: {country}"
        ]
        for pt, country in zip(points, country_names)
    ]
    
    map_obj = folium.Map(location=[45, 10], zoom_start=5, tiles='OpenStreetMap')
    
    # Modify callback to pass the country (row[2]) to the setPointDetails function.
    callback = """
    function(row) {
        var popup = row[3];
        var marker = L.circleMarker([row[0], row[1]], {radius: 10, color: 'green'});
        marker.bindPopup(popup);
        marker.on('click', function() {
            window.setPointDetails(row[0], row[1], row[2]);
        });
        return marker;
    }
    """
    
    FastMarkerCluster(data=marker_data, callback=callback).add_to(map_obj)
    
    return render_template('index.html', map=map_obj)

if __name__ == '__main__':
    app.run(debug=True)