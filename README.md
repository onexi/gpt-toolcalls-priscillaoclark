[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/9wDnMTRl)

# MBTA Train Schedule Application (PS04)

This project is a Flask-based web application that provides train schedule information using data from the MBTA (Massachusetts Bay Transportation Authority). The application accepts user input, interacts with backend Python scripts, and displays train schedule data on the frontend, along with the expected weather at the destination. 

The application leverages OpenAI API tool calling to return a JSON with structured fields from the user's query. The JSON is used to pass parameters into the getTrain.py function. The JSON result of the function from the MBTA API is passed back to OpenAI for interpretation. 

A secondary tool call leverages the latitude, longitude and expected arrival time to tell the user what weather to expect when they get to their destination.

## Project Structure

- **`app.py`**: The main Flask application.
- **`getTrain.py`**: A Python script to fetch train schedule data.
- **`getWeather.py`**: A Python script to fetch weather data related to the station.
- **`main.py`**: A helper script to manage key logic.
- **`index.html`**: The main HTML file that renders the frontend.

## Requirements

The project dependencies are listed in `requirements.txt`. Ensure you have Python 3.x installed on your system before proceeding.

## API Keys

Keys for the MBTA and OpenAI APIs have been added as secrets into the codespaces settings for this repository.

## Setup

1. Ensure python extension is installed in codespaces.

2. Navigate to the `PS04` directory:

   ```bash
   cd PS04
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:

   ```bash
   flask run
   ```

5. Open your web browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

   This will load the frontend page (`index.html`) where you can interact with the app.

## File Details

### app.py

This is the main entry point for the Flask application. It handles routing, including:

- `GET /`: Loads the main page.
- `POST /result`: Processes the user's input and returns the train schedule information.

### getTrain.py

This script retrieves MBTA train schedule data. It interacts with the MBTA API to fetch real-time train arrival and departure information based on user input.

### getWeather.py

This script fetches the current weather conditions at the station the user is interested in. It interacts with a weather API to provide updated data.

### main.py

This file contains additional logic that supports the other scripts, such as error handling and parsing.

### index.html

This is the main frontend of the application. It allows the user to input a message (e.g., train station name) and submit it to get results. It uses Tailwind CSS for styling.
