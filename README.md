# Gemini-Weather-AI-Agent
A beginner AI agent built with Python and Gemini API using manual tool calling to retrieve live weather data through the Open-Meteo API.
# Gemini Weather AI Agent 🌤️

A beginner-level AI agent built with **Python and the Gemini API** using **manual function calling**.

This project was built to understand how an AI model can decide to use a custom tool, how Python executes that tool, and how real-world data can be retrieved from an external API and returned to the AI model.

## 🎯 What This Project Does

The user provides a city name.

Gemini decides whether it needs to use the `get_weather` tool.

The Python program then:

1. Receives the tool call from Gemini.
2. Finds the city's coordinates using the Open-Meteo Geocoding API.
3. Retrieves the current temperature from the Open-Meteo Weather API.
4. Sends the result back to Gemini.
5. Gemini generates the final response.

## 🔄 How It Works

```text
User
  ↓
Gemini API
  ↓
Gemini decides to use get_weather
  ↓
Python executes the tool
  ↓
Open-Meteo Geocoding API
  ↓
City coordinates
  ↓
Open-Meteo Weather API
  ↓
Live temperature
  ↓
Python sends result back to Gemini
  ↓
Gemini final answer
```

## 🧠 Key Concept: Manual Tool Calling

In this project, automatic function calling is disabled.

The Python application manually handles the tool-calling process:

```text
Gemini → Tool Call
       ↓
Python → Execute Tool
       ↓
Python → Send Tool Result
       ↓
Gemini → Final Response
```

This helped me understand what happens behind the scenes when an AI agent uses tools.

## 🛠️ Technologies Used

* Python
* Google Gemini API
* Google GenAI SDK
* Function Calling
* Open-Meteo Geocoding API
* Open-Meteo Weather API
* Requests
* python-dotenv

## 📁 Project Structure

```text
gemini-weather-ai-agent/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd gemini-weather-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named:

```text
.env
```

Add your Gemini API key:

```text
GEMINI_API_KEY=your-api-key
```

Do not upload the `.env` file to GitHub.

### 5. Run the project

```bash
python main.py
```

Example:

```text
You: Hyderabad

Gemini wants to use: get_weather
Arguments: {'city': 'Hyderabad'}

Tool result: The current temperature in Hyderabad is 28.7°C.

Gemini final answer:
The current temperature in Hyderabad is 28.7°C.
```

## 🔐 Security

The Gemini API key is stored in an environment variable and is **not included in the source code**.

The `.env` file is excluded using `.gitignore`.

Never publish a real API key on GitHub.

## 📚 What I Learned

Through this project, I learned:

* What AI agents are at a beginner level
* How Gemini function calling works
* Manual tool calling
* Defining custom tools
* Tool schemas
* How Python executes a requested tool
* How to work with external APIs
* How to retrieve live data
* How to send tool results back to an AI model
* The basic Agent Loop concept
* How API documentation helps find endpoints and parameters

## 🚀 Future Improvements

Planned improvements include:

* Multiple real-world tools
* Sequential tool calling
* Better API error handling
* More tool-selection logic
* Additional external APIs
* Memory and state
* Building a more complete AI agent

## 👩‍💻 About

This is my first beginner-level AI agent project, built as part of my hands-on learning journey in **AI Engineering and AI Automation**.
