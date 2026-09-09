import os
import requests

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# 1. LOAD GEMINI API KEY
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==========================================
# 2. REAL WEATHER TOOL
# ==========================================

def get_weather(city: str):

    # Find the city's coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params
    )

    if geo_response.status_code != 200:
        return "Could not connect to the geocoding service."

    geo_data = geo_response.json()

    if "results" not in geo_data:
        return f"Could not find the city: {city}"

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]


    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    if weather_response.status_code != 200:
        return "Could not retrieve weather data."

    weather_data = weather_response.json()

    temperature = weather_data["current"]["temperature_2m"]

    return f"The current temperature in {city} is {temperature}°C."


# ==========================================
# 3. DESCRIBE THE TOOL TO GEMINI
# ==========================================

weather_tool = types.FunctionDeclaration(
    name="get_weather",
    description="Gets the current live temperature of a city.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "city": types.Schema(
                type="STRING"
            )
        },
        required=["city"]
    )
)


# ==========================================
# 4. CREATE GEMINI TOOL
# ==========================================

tool = types.Tool(
    function_declarations=[
        weather_tool
    ]
)


# ==========================================
# 5. GET USER INPUT
# ==========================================

user_question = input("You: ")


# ==========================================
# 6. CREATE HISTORY
# ==========================================

history = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text=user_question
            )
        ]
    )
]


# ==========================================
# 7. ASK GEMINI
# ==========================================

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=history,
    config=types.GenerateContentConfig(
        tools=[tool],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    )
)


# ==========================================
# 8. CHECK WHETHER GEMINI WANTS THE TOOL
# ==========================================

part = response.candidates[0].content.parts[0]


if part.function_call:

    function_call = part.function_call

    print("\nGemini wants to use:", function_call.name)
    print("Arguments:", function_call.args)


    # ======================================
    # 9. EXECUTE THE PYTHON TOOL
    # ======================================

    if function_call.name == "get_weather":

        result = get_weather(
            **function_call.args
        )

    else:

        result = "Unknown tool"


    print("Tool result:", result)


    # ======================================
    # 10. SAVE GEMINI'S TOOL CALL
    # ======================================

    history.append(
        response.candidates[0].content
    )


    # ======================================
    # 11. SEND TOOL RESULT BACK TO GEMINI
    # ======================================

    history.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": result
                    }
                )
            ]
        )
    )


    # ======================================
    # 12. ASK GEMINI FOR FINAL ANSWER
    # ======================================

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=history,
        config=types.GenerateContentConfig(
            tools=[tool],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )


    print("\nGemini final answer:")
    print(final_response.text)


else:

    print("\nGemini answer:")
    print(response.text)