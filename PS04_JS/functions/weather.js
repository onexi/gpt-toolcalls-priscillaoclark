import { fetchWeatherApi } from 'openmeteo';
// https://openweathermap.org/current
	
const execute = async (latitude, longitude) => {
    const apiKey = process.env.OPENWEATHERMAP_API_KEY; // Fetch API key from Codespaces secret
    if (!apiKey) {
      throw new Error('API key is missing. Make sure OPENWEATHERMAP_API_KEY is set as a Codespaces secret.');
    }

    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;
  
    try {
      const response = await fetch(apiUrl);
      // Log the status code and response for debugging
      console.log(`Response status: ${response.status}`);
      
      if (!response.ok) {
        const errorDetails = await response.text(); // Capture the error details from the response body
        throw new Error(`Weather data could not be fetched. Details: ${errorDetails}`);
      }
  
      const weatherData = await response.json();
      return weatherData;
  
    } catch (error) {
      console.error('Error fetching weather data:', error);
      return null;
    }
}

const details = {
    "type": "function",
    function:{
    "name": "weather",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "string",
                "description": "the latitude of the location",
            },
            "longitude": {
                "type": "string",
                "description": "the longitude of the location",
            },
        },
        "required": ["latitude", "longitude"],
    },
},
    "description": "Given a latitude and longitude, this function returns the current weather data.",
};
export { execute, details };
