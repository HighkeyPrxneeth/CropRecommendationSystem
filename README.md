# Crop Recommendation System

## Description

This project implements a web-based system that recommends suitable crops for a specific geographical location (latitude, longitude) and a target date. It integrates local soil properties (N, P, K, pH) from the LUCAS dataset with predicted weather conditions (temperature, rainfall) derived from historical data using machine learning models (XGBoost). A K-Nearest Neighbors model then uses this combined environmental data to suggest an appropriate crop based on a reference dataset. The system features an interactive map interface built with Flask and Folium.

## Features

*   **Interactive Map Interface:** Uses Folium to display soil data points on a map. Users can click on points to select coordinates.
*   **Soil Data Integration:** Retrieves N, P, K, and pH values for selected coordinates from the LUCAS Soil dataset. Handles missing values via mean imputation.
*   **Historical Weather Fetching:** Uses the Open-Meteo API to gather 30 years of historical daily temperature and rainfall data for the selected location.
*   **Weather Prediction:** Employs XGBoost regression models trained on historical data to predict mean temperature and rainfall sum for a user-specified future date. Includes feature engineering for time, cyclical patterns, seasonality, and rainfall lag/rolling features.
*   **Crop Recommendation:** Utilizes a K-Nearest Neighbors (KNN) classifier trained on a dataset linking environmental factors to crops. Recommends a crop based on soil data and predicted weather.
*   **Web Application:** Built with Flask, providing a user interface to interact with the system.

## Technology Stack

*   **Backend:** Python, Flask
*   **Machine Learning:** Scikit-learn (KNeighborsClassifier), XGBoost (XGBRegressor)
*   **Data Handling:** Pandas, NumPy
*   **Geospatial:** Geopandas, Shapely, Folium
*   **APIs & Data:** Open-Meteo API, LUCAS Soil Dataset (`LUCAS_SOIL.csv`), Crop Recommendation Dataset (`Crop_recommendation.csv`), Natural Earth Shapefiles
*   **API Interaction:** openmeteo-requests, requests-cache, retry-requests

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/HighkeyPrxneeth/CropRecommendationSystem.git
    cd ML-Project
    ```
2.  **Create a virtual environment:**
    ```bash
    conda env create -f environment.yml\
    conda activate crops
    ```
3.  **Ensure Data Files are Present:**
    *   Make sure the `resources` directory exists in the project root.
    *   Place the required data files inside `resources`:
        *   `LUCAS_SOIL.csv`
        *   `Crop_recommendation.csv`
        *   Natural Earth shapefile components (e.g., `ne_10m_admin_0_countries.shp`, `.dbf`, `.shx`, etc.)

## Usage

1.  **Run the Flask application:**
    ```bash
    python main.py
    ```
2.  **Access the application:** Open your web browser and navigate to `http://127.0.0.1:5000` (or the address provided by Flask).
3.  **Interact with the map:**
    *   Browse the map displaying soil data points.
    *   Click on a green marker representing a soil data point. This will populate the Latitude and Longitude fields in the form.
4.  **Enter Date:** Select the target date for the crop recommendation using the date input field.
5.  **Get Recommendation:** Click the "Get Recommendation" button (or similar).
6.  **View Result:** The system will process the request (fetch weather, predict conditions, query soil data, predict crop) and display the recommended crop below the form.

## Data Sources

*   **Soil Data:** LUCAS 2018 Soil dataset (via `resources/LUCAS_SOIL.csv`). Requires appropriate citation if used publicly.
*   **Weather Data:** Open-Meteo Historical Weather API ([https://open-meteo.com/](https://open-meteo.com/)). Fetches 30 years of daily data.
*   **Crop Suitability Data:** Provided via `resources/Crop_recommendation.csv`. (Specify origin if known).
*   **Geospatial Boundaries:** Natural Earth Admin 0 Countries dataset ([https://www.naturalearthdata.com/](https://www.naturalearthdata.com/)).

## Project Structure

```
.
├── main.py             # Flask application, main logic orchestration
├── models.py           # Defines WeatherModel (XGBoost) and CropModel (KNN)
├── soil.py             # Handles LUCAS soil data loading and querying (SoilData class)
├── weather.py          # Handles Open-Meteo API interaction (Weather class)
├── requirements.txt    # Project dependencies (needs to be created)
├── templates/
│   └── index.html      # HTML template for the web interface (structure assumed)
├── resources/
│   ├── LUCAS_SOIL.csv  # LUCAS dataset
│   ├── Crop_recommendation.csv # Crop recommendation training data
│   └── ne_10m_admin_0_countries.* # Shapefiles for country lookup
└── README.md           # This file
```

## Future Work

*   **Pre-train Models:** Train weather and crop models offline and load them in the Flask app instead of retraining on each request for efficiency.
*   **Improve Weather Forecasting:** Explore time-series models like ARIMA or LSTMs.
*   **Enhance Crop Model:** Use more advanced classifiers (Random Forest, Gradient Boosting) and incorporate more features (soil type, sunlight).
*   **Better Imputation:** Use more sophisticated methods (e.g., spatial interpolation) for missing soil data.
*   **Expand Data:** Incorporate higher-resolution soil data or data for other regions.
*   **Deployment:** Containerize the application (e.g., using Docker) for easier deployment.
