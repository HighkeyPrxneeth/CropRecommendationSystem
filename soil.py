import pandas as pd

class Soil:
    def __init__(self, lat, long):
        self.N, self.P, self.K, self.pH  = SoilData().get_data(lat, long)
        self.data = (self.N, self.P, self.K, self.pH)
        if self.N is None or self.P is None or self.K is None or self.pH is None:
            raise ValueError("Data not found")

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
        try:
            self.N = self.df[(self.df['th_lat'] == lat) & (self.df['th_long'] == long)]["N"].iloc[0]
            self.P = self.df[(self.df['th_lat'] == lat) & (self.df['th_long'] == long)]["P"].iloc[0]
            self.K = self.df[(self.df['th_lat'] == lat) & (self.df['th_long'] == long)]["K"].iloc[0]
            self.pH = self.df[(self.df['th_lat'] == lat) & (self.df['th_long'] == long)]["pH_H2O"].iloc[0]
        except:
            self.N = None
            self.P = None
            self.K = None
            self.pH = None
        return self.N, self.P, self.K, self.pH
    
    def get_points(self):
        return self.df["th_lat"], self.df["th_long"]