import os
import openai
import json
from datetime import datetime, timedelta
import json
import requests
from datetime import datetime
from getTrain import getTrain
from getWeather import getWeather

#user_message = "When is the next train from South Station to Kendall Square?"

def main(user_message):

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MBTA_KEY = os.getenv('MBTA_KEY')

    # Initial call to OpenAI API

    # Prompt the user in the terminal
    #user_message = input("Please enter your question about MBTA trains: ")
    #user_message = "When is the next train from South Station to Kendall Square?"

    # Set system prompt and tell it the correct current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_message = f"You are a helpful assistant which looks for Boston MBTA transit information and will tell the user the expected weather for their arrival. The current datetime is {current_time}."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}]

    # Build the transit tool schema
    transit_tool = [
        {
            "type": "function",
            "function": {
            "name": "get_transit_info",
            "description": "Get next train information for a given station",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_station": {
                        "type": "string",
                        "description": "The departing station, e.g. Kendall Square",
                    },
                    "mbta_departure_station_id": {
                        "type": "string",
                        "description": "The departing station ID, e.g. place-kndl",
                    },
                    "destination_station": {
                        "type": "string",
                        "description": "The destination station, e.g. South Station",
                    },
                    "mbta_destination_station_id": {
                        "type": "string",
                        "description": "The destination station ID, e.g. place-alfcl",
                    },
                    "train_date": {
                        "type": "string",
                        "description": "The start date of the train to search",
                    },
                    "train_unix_time": {
                        "type": "integer",
                        "description": "The start date of the train to search in unix format",
                    },
                    "current_unix_time": {
                        "type": "integer",
                        "description": "The current datetime in unix format",
                    },
                    "destination_latitude": {
                        "type": "string",
                        "description": "Latitude of the destination station",
                    },
                    "destination_longitude": {
                        "type": "string",
                        "description": "Longitude of the destination station",
                    },
                },
                "required": ["departure_station", "mbta_departure_station_id", "destination_station", "mbta_destination_station_id", "train_date", "train_unix_time", "current_unix_time", "destination_latitude", "destination_longitude"],
            },
        }
        }
    ]

    # Call the OpenAI API with the transit tool
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=transit_tool,
    )
    tool_call = response.choices[0].message.tool_calls[0]
    arguments = tool_call.function.arguments
    dict_arguments = json.loads(arguments)

    departure_id = dict_arguments['mbta_departure_station_id']
    next_train = getTrain(departure_id, current_time, MBTA_KEY)
    next_train = json.dumps(next_train)

    # Build the weather tool
    weather_tool = [
        {
            "type": "function",
            "function": {
            "name": "get_weather_at_time",
            "description": "Get the weather forecast for a specific location and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "arrival_time": {
                        "type": "string",
                        "description": "The arrival time to the destination",
                    },
                    "destination_latitude": {
                        "type": "string",
                        "description": "Latitude of the destination station",
                    },
                    "destination_longitude": {
                        "type": "string",
                        "description": "Longitude of the destination station",
                    },
                },
                "required": ["arrival_time", "destination_latitude", "destination_longitude"],
            },
        }
        }
    ]

    # Call the OpenAI API with the weather tool
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
        {"role": "system", "content": next_train}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=weather_tool,
    )

    # Final response might have a tool call or it might ask if you want to see the weather - automatically respond with yes
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = tool_call.function.arguments
        dict_arguments = json.loads(arguments)
        
        arrival_time = dict_arguments['arrival_time']
        try:
            arrival_time = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S%z")
        except:
            arrival_time = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S")
        arrival_time = arrival_time.strftime("%Y-%m-%dT%H:%M")

        destination_latitude = dict_arguments['destination_latitude']
        destination_longitude = dict_arguments['destination_longitude']

        weather_data = getWeather(float(destination_latitude), float(destination_longitude), arrival_time)
        weather_data = json.dumps(weather_data)

        # Call final response with all context and return the output
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
            {"role": "system", "content": next_train},
            {"role": "system", "content": weather_data}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        output = response.choices[0].message.content
        return output
        
    else:
        
        user_response = 'Yes. Provide me with the weather forecast for my arrival and repeat the train information.'
        messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
        {"role": "system", "content": next_train},
        {"role": "system", "content": user_response},
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=weather_tool,
        )
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = tool_call.function.arguments
        dict_arguments = json.loads(arguments)
            
        # Wrangle the dates
        arrival_time = dict_arguments['arrival_time']
        arrival_time = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S%z")
        arrival_time = arrival_time.strftime("%Y-%m-%dT%H:%M")
        
        # Pull coordinates of the destination
        destination_latitude = dict_arguments['destination_latitude']
        destination_longitude = dict_arguments['destination_longitude']

        weather_data = getWeather(float(destination_latitude), float(destination_longitude), arrival_time)
        weather_data = json.dumps(weather_data)
        
        # Call final response with all context and return the output
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
            {"role": "system", "content": next_train},
            {"role": "system", "content": weather_data}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        output = response.choices[0].message.content
        return output



