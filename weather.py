import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import time

cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

class Weather:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.url = "https://archive-api.open-meteo.com/v1/archive"
        self.end_date = time.strftime("%Y-%m-%d")
        self.start_date = pd.to_datetime(self.end_date) - pd.DateOffset(years = 30)
        self.start_date = self.start_date.strftime("%Y-%m-%d")
        self.params = {
            "latitude": self.lat,
            "longitude": self.long,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "daily": ["temperature_2m_mean", "rain_sum"]
        }
        self.responses = openmeteo.weather_api(self.url, params = self.params)
        self.data = self.get_weather()
    def get_weather(self):
        response = self.responses[0]
        daily = response.Daily()
        daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(1).ValuesAsNumpy()
        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
        daily_data["rain_sum"] = daily_rain_sum
        daily_dataframe = pd.DataFrame(data = daily_data)
        daily_dataframe = daily_dataframe.dropna()
        return daily_dataframe
