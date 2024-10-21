[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/9wDnMTRl)

# Two Solutions Provided (See folders PS04_JS and PS04_PY)

## 1. Updates to L04 (PS04_JS)

New weather.js function uses https://openweathermap.org/ API to pull current weather for a specified latitude and longitude. OpenAI returns the latitude and longitude for a city requested in the user's prompt and feeds it into the function using tool call. The OPENWEATHERMAP_API_KEY is loaded as a secret into codespaces.

## 2. MBTA Train Schedule Application (PS04_PY)

This project is a Flask-based web application that provides train schedule information using data from the MBTA (Massachusetts Bay Transportation Authority). The application accepts user input, interacts with backend Python scripts, and displays train schedule data on the frontend. 

The application leverages OpenAI API tool calling to return a JSON with structured fields from the user's query. The JSON is used to pass parameters into the getTrain.py function. The JSON result of the function from the MBTA API is passed back to OpenAI for interpretation and response to the user.
