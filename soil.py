import pandas as pd
import numpy as np

class Soil:
    def __init__(self, lat, long):
        lat = float(lat)
        long = float(long)
        self.N, self.P, self.K, self.pH  = SoilData().get_data(lat, long)
        self.data = (self.N, self.P, self.K, self.pH)
        if self.N is None or self.P is None or self.K is None or self.pH is None:
            raise ValueError(f"Data not found, ph: {self.pH}, N: {self.N}, P: {self.P}, K: {self.K}")

    def get_data(self):
        return self.data

class SoilData:
    def __init__(self):
        self.df = pd.read_csv("LUCAS_SOIL.csv").drop_duplicates()

        self.df["N"] = pd.to_numeric(self.df["N"], errors="coerce")
        self.df["P"] = pd.to_numeric(self.df["P"], errors="coerce")
        self.df["K"] = pd.to_numeric(self.df["K"], errors="coerce")
        self.df["pH_H2O"] = pd.to_numeric(self.df["pH_H2O"], errors="coerce")

        self.N = None
        self.P = None
        self.K = None
        self.pH = None

        self.df["N"] = self.df["N"].fillna(self.df["N"].mean())
        self.df["P"] = self.df["P"].fillna(self.df["P"].mean())
        self.df["K"] = self.df["K"].fillna(self.df["K"].mean())
        self.df["pH_H2O"] = self.df["pH_H2O"].fillna(self.df["pH_H2O"].mean())
    
    def get_data(self, lat, long):
        mask = np.isclose(self.df['th_lat'], lat) & np.isclose(self.df['th_long'], long)
        self.N = self.df[mask]["N"].iloc[0]
        self.P = self.df[mask]["P"].iloc[0]
        self.K = self.df[mask]["K"].iloc[0]
        self.pH = self.df[mask]["pH_H2O"].iloc[0]
        return self.N, self.P, self.K, self.pH
    
    def get_points(self):
        return self.df["th_lat"], self.df["th_long"]