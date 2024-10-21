async function getWeather(latitude, longitude) {
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
  

  // Example usage:
  getWeather(40.7128, -74.0060) // Latitude and Longitude for New York
    .then(data => {
      if (data) {
        console.log('Weather data:', data);
      }
    })
    .catch(err => console.error(err));
