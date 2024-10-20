import requests
from datetime import datetime

def getWeather(latitude, longitude, datetime_str):
    """
    Fetches weather forecast from Open-Meteo API for the given latitude, longitude, and datetime.
    Returns temperature in Celsius and Fahrenheit, along with precipitation amount.

    Parameters:
    lat (float): Latitude of the location.
    lon (float): Longitude of the location.
    datetime_str (str): The date and time in ISO 8601 format (YYYY-MM-DDTHH:MM).

    Returns:
    dict: Dictionary with temperature in Celsius, Fahrenheit, and precipitation amount.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Convert the input datetime string to the appropriate format if needed
    forecast_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start": forecast_time.isoformat(),  # Start time for the forecast
        "end": forecast_time.isoformat(),    # End time can be the same for a specific time forecast
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto"
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'hourly' in data and 'temperature_2m' in data['hourly'] and 'precipitation' in data['hourly']:
            temp_c = data['hourly']['temperature_2m'][0]  # Assuming first hour matches the requested time
            precipitation = data['hourly']['precipitation'][0]  # Precipitation at the same time
            
            # Convert temperature from Celsius to Fahrenheit
            temp_f = (temp_c * 9/5) + 32

            return {
                "temperature_celsius": temp_c,
                "temperature_fahrenheit": temp_f,
                "precipitation": precipitation
            }
        else:
            return {"error": "Weather data unavailable for the requested time"}
    else:
        return {"error": "Failed to fetch weather data", "status_code": response.status_code}