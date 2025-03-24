import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from xgboost import XGBRegressor

class CropModel:
    def __init__(self):
        self.data = pd.read_csv("Crop_recommendation.csv").drop('humidity', axis=1)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self):
        X = self.data.drop('label', axis=1)
        y = self.data['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.model.fit(X_train, y_train)
        self.X_test, self.y_test = X_test, y_test

    def score(self):
        return f1_score(self.y_test, self.model.predict(self.X_test), average='weighted')

    def predict(self, X):
        return self.model.predict(X)

class WeatherModel:
    def __init__(self, df):
        self.df = df.copy()
        self.temp_model = RandomForestRegressor(max_depth=100, random_state=42, n_estimators=100)
        self.rain_model = XGBRegressor(random_state=42, n_estimators=200, learning_rate=0.1)
        self.rain_lag_fill = None
        self.rain_roll3_fill = None
        self.rain_roll_std_fill = None

    def preprocess(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.sort_values('date', inplace=True)
        self.df['day'] = self.df['date'].dt.day
        self.df['month'] = self.df['date'].dt.month
        self.df['year'] = self.df['date'].dt.year
        self.df['month_sin'] = np.sin(2 * np.pi * self.df['month'] / 12)
        self.df['month_cos'] = np.cos(2 * np.pi * self.df['month'] / 12)
        self.df['day_sin'] = np.sin(2 * np.pi * self.df['day'] / 31)
        self.df['day_cos'] = np.cos(2 * np.pi * self.df['day'] / 31)
        self.df['season'] = self.df['month'].apply(lambda m: 'winter' if m in [12,1,2]
                                                  else ('spring' if m in [3,4,5]
                                                  else ('summer' if m in [6,7,8] else 'fall')))
        self.df = pd.get_dummies(self.df, columns=['season'], drop_first=True)
        basic_features = ['day', 'month', 'year', 'month_sin', 'month_cos', 'day_sin', 'day_cos']
        basic_features.extend([col for col in self.df.columns if col.startswith('season_')])
        self.df['rain_lag1'] = self.df['rain_sum'].shift(1)
        self.df['rain_lag2'] = self.df['rain_sum'].shift(2)
        self.df['rain_roll3'] = self.df['rain_sum'].rolling(window=3).mean()
        self.df['rain_roll_std'] = self.df['rain_sum'].rolling(window=3).std()
        self.df.bfill(inplace=True)
        self.rain_lag_fill = self.df['rain_sum'].mean()
        self.rain_roll3_fill = self.df['rain_roll3'].mean()
        self.rain_roll_std_fill = self.df['rain_roll_std'].mean()
        self.temp_features_list = basic_features
        self.rain_features_list = basic_features + ['rain_lag1', 'rain_lag2', 'rain_roll3', 'rain_roll_std']
        self.df.drop(columns=['date'], inplace=True)

    def fit(self):
        self.preprocess()
        temp_features = self.df[self.temp_features_list]
        rain_features = self.df[self.rain_features_list]
        X_temp_train, X_temp_test, y_temp_train, y_temp_test = train_test_split(
            temp_features, self.df['temperature_2m_mean'], test_size=0.3, random_state=42)
        X_rain_train, X_rain_test, y_rain_train, y_rain_test = train_test_split(
            rain_features, self.df['rain_sum'], test_size=0.3, random_state=42)
        self.temp_model.fit(X_temp_train, y_temp_train)
        self.rain_model.fit(X_rain_train, y_rain_train)
        self.X_temp_test, self.y_temp_test = X_temp_test, y_temp_test
        self.X_rain_test, self.y_rain_test = X_rain_test, y_rain_test
        print(self.score())

    def score(self):
        return {
            "temperature_model": self.temp_model.score(self.X_temp_test, self.y_temp_test),
            "rain_model": self.rain_model.score(self.X_rain_test, self.y_rain_test)
        }

    def predict(self, day, month, year):
        basic = {'day': [day], 'month': [month], 'year': [year]}
        df_basic = pd.DataFrame(basic)
        df_basic['month_sin'] = np.sin(2 * np.pi * df_basic['month'] / 12)
        df_basic['month_cos'] = np.cos(2 * np.pi * df_basic['month'] / 12)
        df_basic['day_sin'] = np.sin(2 * np.pi * df_basic['day'] / 31)
        df_basic['day_cos'] = np.cos(2 * np.pi * df_basic['day'] / 31)
        df_basic['season'] = df_basic['month'].apply(lambda m: 'winter' if m in [12,1,2]
                                                     else ('spring' if m in [3,4,5]
                                                     else ('summer' if m in [6,7,8] else 'fall')))
        df_basic = pd.get_dummies(df_basic, columns=['season'], drop_first=True)
        for col in self.temp_features_list:
            if col not in df_basic.columns:
                df_basic[col] = 0
        df_basic = df_basic[self.temp_features_list]
        temp_pred = self.temp_model.predict(df_basic)[0]
        df_rain = df_basic.copy()
        for col in ['rain_lag1', 'rain_lag2']:
            df_rain[col] = self.rain_lag_fill
        df_rain['rain_roll3'] = self.rain_roll3_fill
        df_rain['rain_roll_std'] = self.rain_roll_std_fill
        df_rain = df_rain[self.rain_features_list]
        rain_pred = self.rain_model.predict(df_rain)[0]
        return temp_pred, rain_pred
