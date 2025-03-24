import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_world_points(lat_series: pd.Series, lon_series: pd.Series):
    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([-25, 45, 34, 72], crs=ccrs.PlateCarree())

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    
    ax.plot(lon_series, lat_series, 'ro', markersize=1, transform=ccrs.PlateCarree())
    
    plt.title("World Map Plot")
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv("LUCAS_SOIL.csv")

    lat_series = df["th_lat"]
    lon_series = df['th_long']
    df = df[["th_lat", "th_long", "pH_H2O", "N", "P", "K"]]
    print(df.columns)
    print(df.info())

    df.to_csv("LUCAS_SOIL.csv", index=False)
    print(f"Points found: {len(lat_series)}")
    
    plot_world_points(lat_series, lon_series)
