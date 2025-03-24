from soil import Soil
from weather import Weather
from models import CropModel, WeatherModel
import pandas as pd

lat = 48.58112
long = 14.94929

soil = Soil(lat, long)
weather = Weather(lat, long)

weather_model = WeatherModel(weather.data)
weather_model.fit()

