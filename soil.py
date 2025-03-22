import requests

class Soil:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        url = "https://SDMDataAccess.sc.egov.usda.gov/Tabular/post.rest"
        data = {
            "format": "JSON",
            "query": f"SELECT mukey, phh2o, total_n, p_mehlich3, k_nh4_ph_7 FROM chorizon WHERE mukey IN (SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('point({self.lat} {self.long})'))"
        }
        response = requests.post(url, data=data)
        result = response.json()
        self.pH = result["Table"][0]["phh2o"]
        self.N = result["Table"][0]["total_n"]
        self.P = result["Table"][0]["p_mehlich3"]
        self.K = result["Table"][0]["k_nh4_ph_7"]
    def get_data(self):
        return self.pH, self.N, self.P, self.K