# Lab Assignment 4 Solutions
# Zeina Ayman - 202200351
# Conversational Agents with Tool Use and Reasoning Techniques

## Description
This project implements a **Conversational Agent** that can interact with users, use external APIs, and apply reasoning techniques like **Chain of Thought (CoT)** and **ReAct (Reasoning + Acting)** paradigms. The agent supports:
- Fetching **real-time weather data**
- Performing **mathematical calculations**
- Conducting **web searches** (simulated)
- Reasoning through **CoT** and **ReAct** approaches
## Setup Instructions
### 1. Clone the Repository
git clone https://github.com/your-repo-name.git
cd your-repo-name
### 2. Install Dependencies
pip install -r requirements.txt
### 3. Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
API_KEY=your_openai_api_key
BASE_URL=your_openai_base_url
LLM_MODEL=your_model
WEATHER_API_KEY=your_weather_api_key
### 4. Run the Agent
python conversational_agent.py
You will be prompted to select an agent type:
- **1:** Basic Weather Assistant
- **2:** Chain of Thought Agent
- **3:** ReAct Agent
## Features
### Basic Functionality
- Retrieves real-time **weather data**
- Provides **weather forecasts**
### Advanced Reasoning
- **Chain of Thought (CoT):** Uses a step-by-step approach to solve problems.
- **ReAct:** Dynamically determines whether to use weather, calculator, or web search tools to provide the best response.
## Example Conversations
### Basic Agent:
You: What's the weather in Paris?
Assistant: The temperature in Paris is 18°C with clear skies.
### Chain of Thought Agent:
You: What is 5 times the current temperature in New York?
Assistant: 
1. First, I will fetch the temperature in New York.
2. The temperature is 10°C.
3. Now, I calculate 5 * 10.
Final Answer: 50.
### ReAct Agent:
You: How does climate change affect temperature?
Assistant:
1. Thought: I should search for information on climate change.
2. Action: Performing a web search.
3. Observation: Climate change refers to significant temperature shifts.
Final Answer: Climate change leads to global temperature shifts over time.
