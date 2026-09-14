# 🌦️ Weather API 

## 📌 Project Overview

This project is a **Weather AI application** built using **Hugging Face LLMs, Function Calling, Streamlit, and Open-Meteo APIs**.

The application allows users to ask questions about the weather in a city. The LLM identifies when weather information is required, calls the `get_weather(city)` Python function, and the function fetches real-time weather data from Open-Meteo.

## 🌐 Live Demo

🚀 Link: https://weather-api-2wfc23dpug8pecwepxfjbz.streamlit.app/

## 🎯 Objectives

* Understand Function Calling in LLMs
* Integrate Hugging Face `InferenceClient`
* Define and use tools with an LLM
* Fetch city coordinates using the Open-Meteo Geocoding API
* Fetch real-time weather information
* Send tool results back to the LLM
* Display the final response using Streamlit

## 🏗️ Architecture

```text
User
  ↓
Hugging Face LLM
  ↓
Function Call: get_weather(city)
  ↓
Python Function
  ↓
Open-Meteo Geocoding API
  ↓
Open-Meteo Weather API
  ↓
Weather Data
  ↓
LLM
  ↓
Final Weather Response
```

## 🛠️ Technologies Used

* Python
* Streamlit
* Hugging Face
* Hugging Face InferenceClient
* Open-Meteo Geocoding API
* Open-Meteo Forecast API
* Requests
* JSON
* Function Calling

## 📂 Project Structure

```text
Weather-API/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-github-repository-link>
cd Weather-API
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## 🔑 Hugging Face Token

Create a Hugging Face Access Token and store it securely in:

```text
.streamlit/secrets.toml
```

Add:

```toml
HF_TOKEN = "your_hugging_face_token"
```

⚠️ **Never upload `secrets.toml` to GitHub.**

Add it to `.gitignore`:

```text
.streamlit/secrets.toml
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 💬 Example

User:

```text
What is the current weather in Chennai?
```

The LLM can call:

```text
get_weather("Chennai")
```

The Python function fetches the weather data from Open-Meteo and sends the result back to the LLM.

The application then displays a natural-language weather response.

## 🔄 How Function Calling Works

1. The user asks a weather-related question.
2. The LLM receives the question and the available `get_weather` tool.
3. The LLM generates a structured function call.
4. Python executes the `get_weather()` function.
5. The function uses the Open-Meteo Geocoding API to find the city coordinates.
6. The Open-Meteo Forecast API provides the weather information.
7. The weather data is returned as a tool result.
8. The tool result is sent back to the LLM.
9. The LLM generates the final response for the user.

## 🌐 APIs Used

### Open-Meteo Geocoding API

Used to convert a city name into latitude and longitude coordinates.

### Open-Meteo Forecast API

Used to retrieve current weather information such as:

* Temperature
* Humidity
* Wind Speed

## 🤖 Hugging Face Model

The application uses:

```text
Qwen/Qwen2.5-72B-Instruct
```

through the Hugging Face `InferenceClient`.

## 🔐 Security

The Hugging Face API token is stored using Streamlit Secrets.

The following file should **not** be committed to GitHub:

```text
.streamlit/secrets.toml
```

## 🚀 Future Improvements

* Add weather forecasts for multiple days
* Add weather icons
* Add temperature unit selection
* Add more weather parameters
* Improve the user interface
* Deploy the application online

## 📚 Learning Outcome

This project demonstrates how an LLM can work together with Python functions and external APIs.

The main workflow is:

```text
LLM decides → Python executes → API fetches → LLM responds
```
