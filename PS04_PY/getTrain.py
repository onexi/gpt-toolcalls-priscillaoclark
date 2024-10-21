import requests

# Function to get next train from Kendall Square to Alewife
def getTrain(departure_id, current_time, MBTA_KEY):
    # API endpoint
    url = "https://api-v3.mbta.com/predictions"
    
    # Parameters for the request
    params = {
        "filter[stop]": departure_id,  # Station ID
        #"filter[direction_id]": direction_id,  # Direction ID
        "sort": "departure_time",  # Sort by upcoming departures
        "api_key": MBTA_KEY,  # Your API key
        "include": "stop", 
    }
    
    # Send GET request to the MBTA API
    response = requests.get(url, params=params)
    #response = requests.get("https://api-v3.mbta.com/predictions?filter%5Bstop%5D=place-sstat&filter%5Bdirection_id%5D=0&include=stop")
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data = response.json()

    return data