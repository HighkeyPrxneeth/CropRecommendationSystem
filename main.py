from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from soil import SoilData
from folium.plugins import FastMarkerCluster

app = Flask(__name__)

world = gpd.read_file("resources\\ne_10m_admin_0_countries.shp")

def get_countries_bulk(points):
    gdf_points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in points], crs=world.crs)
    joined = gpd.sjoin(gdf_points, world, how="left", predicate="within")
    return joined["NAME"].fillna("Unknown").tolist()

@app.route('/')
def index():
    lat_series, lon_series = SoilData().get_points()
    points = list(zip(lat_series.values, lon_series.values))
    country_names = get_countries_bulk(points)
    
    marker_data = [
        [
            pt[0],
            pt[1],
            f"Latitude: {pt[0]}<br>Longitude: {pt[1]}<br>Country: {country}"
        ]
        for pt, country in zip(points, country_names)
    ]
    
    map_obj = folium.Map(location=[45, 10], zoom_start=5, tiles='OpenStreetMap')
    
    callback = """
    function(row) {
         var popup = row[2];
         var marker = L.circleMarker([row[0], row[1]], {radius: 10, color: 'green'});
         marker.bindPopup(popup);
         return marker;
    }
    """
    
    FastMarkerCluster(data=marker_data, callback=callback).add_to(map_obj)
    
    return render_template('index.html', map=map_obj)

if __name__ == '__main__':
    app.run(debug=True)