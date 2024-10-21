import os
import openai
import json
from datetime import datetime, timedelta
import json
import requests
from datetime import datetime
from getTrain import getTrain

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
    system_message = f"You are a helpful assistant which looks for Boston MBTA transit information. The current datetime is {current_time}."

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
                },
                "required": ["departure_station", "mbta_departure_station_id", "destination_station", "mbta_destination_station_id", "train_date", "train_unix_time", "current_unix_time"],
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

    # Call the OpenAI API again and provide it with the train information
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
        {"role": "system", "content": next_train}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    output = response.choices[0].message.content
    return output


