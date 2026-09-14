import streamlit as st
import os
import json
import requests
from huggingface_hub import InferenceClient

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Weather AI",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Weather AI")
st.write("Ask about the current weather of any city.")

# ---------------------------------------------------
# Hugging Face Token
# ---------------------------------------------------

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    st.error("HF_TOKEN is missing. Please add it to Streamlit Secrets.")
    st.stop()

# ---------------------------------------------------
# Hugging Face Client
# ---------------------------------------------------

client = InferenceClient(
    api_key=HF_TOKEN
)

# ---------------------------------------------------
# Weather Function
# ---------------------------------------------------

def get_weather(city):
    try:
        # Step 1: Get latitude and longitude
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "format": "json"
            },
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            return {
                "error": f"Could not find the city: {city}"
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get current weather
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        return {
            "city": location.get("name", city),
            "country": location.get("country", ""),
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"]
        }

    except requests.RequestException as e:
        return {
            "error": f"Weather API error: {str(e)}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }


# ---------------------------------------------------
# Function Calling Tool
# ---------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather information for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# ---------------------------------------------------
# User Input
# ---------------------------------------------------

question = st.chat_input("Ask about the weather...")

if question:

    st.chat_message("user").write(question)

    # ------------------------------------------------
    # First LLM Call
    # ------------------------------------------------

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    try:

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # ------------------------------------------------
        # Check for Function Call
        # ------------------------------------------------

        if message.tool_calls:

            tool = message.tool_calls[0]

            args = json.loads(
                tool.function.arguments
            )

            city = args["city"]

            # ------------------------------------------------
            # Execute Python Function
            # ------------------------------------------------

            result = get_weather(city)

            # Display weather data
            if "error" in result:

                st.error(result["error"])
                st.stop()

            # ------------------------------------------------
            # Send Tool Result Back to LLM
            # ------------------------------------------------

            messages.append(message)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": json.dumps(result)
                }
            )

            # ------------------------------------------------
            # Second LLM Call
            # ------------------------------------------------

            final_response = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages
            )

            answer = final_response.choices[0].message.content

            # ------------------------------------------------
            # Display Final Answer
            # ------------------------------------------------

            with st.chat_message("assistant"):
                st.write(answer)

        else:

            with st.chat_message("assistant"):
                st.write(message.content)

    except Exception as e:

        st.error(f"Error: {str(e)}")