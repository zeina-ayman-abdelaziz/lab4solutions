# Lab Assignment 4 Solutions
# Zeina Ayman - 202200351
import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
LLM_MODEL = os.environ.get("LLM_MODEL")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
# Weather Tools
def get_current_weather(location):
    """Get the current weather for a location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    weather_info = data["current"]
    return json.dumps({
        "location": data["location"]["name"],
        "temperature_c": weather_info["temp_c"],
        "condition": weather_info["condition"]["text"]
    })
def get_weather_forecast(location, days=3):
    """Get a weather forecast for a location."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    forecast_days = data["forecast"]["forecastday"]
    return json.dumps({
        "location": data["location"]["name"],
        "forecast": [{
            "date": day["date"],
            "max_temp_c": day["day"]["maxtemp_c"],
            "condition": day["day"]["condition"]["text"]
        } for day in forecast_days]
    })
# Calculator Tool
def calculator(expression):
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"
# Web Search Tool (Simulated)
def web_search(query):
    """Simulate a web search."""
    search_results = {
        "weather forecast": "Weather forecasts include temperature, precipitation, wind speed, etc.",
        "temperature conversion": "Celsius to Fahrenheit: multiply by 9/5 and add 32.",
        "climate change": "Climate change refers to significant global temperature and climate shifts."
    }
    return json.dumps({"query": query, "result": search_results.get(query.lower(), "No relevant information found.")})
# Tool Definitions
weather_tools = [
    {"type": "function", "function": {"name": "get_current_weather", "parameters": {"location": "string"}}},
    {"type": "function", "function": {"name": "get_weather_forecast", "parameters": {"location": "string", "days": "integer"}}}
]
calculator_tool = {"type": "function", "function": {"name": "calculator", "parameters": {"expression": "string"}}}
search_tool = {"type": "function", "function": {"name": "web_search", "parameters": {"query": "string"}}}
# Combine Tools
cot_tools = weather_tools + [calculator_tool]
react_tools = cot_tools + [search_tool]
# Available Function Mapping
available_functions = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "calculator": calculator,
    "web_search": web_search
}
# Message Processing
def process_messages(client, messages, tools=None, available_functions=None):
    response = client.chat.completions.create(
        model=LLM_MODEL, messages=messages, tools=tools or []
    )
    response_message = response.choices[0].message
    messages.append(response_message)
    
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": function_response})
    
    return messages
# Conversation Manager
def run_conversation(client, system_message):
    messages = [{"role": "system", "content": system_message}]
    print("Assistant: Hello! Ask me about weather, calculations, or general information.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Assistant: Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        messages = process_messages(client, messages, tools=react_tools, available_functions=available_functions)
        last_message = messages[-1]
        if last_message.get("content"):
            print(f"Assistant: {last_message['content']}")
# Run the Agent
if __name__ == "__main__":
    choice = input("Choose an agent type (1: Basic, 2: Chain of Thought, 3: ReAct): ")
    system_message = "You are a helpful assistant."
    tools = weather_tools
    if choice == "2":
        system_message = "Use Chain of Thought reasoning."
        tools = cot_tools
    elif choice == "3":
        system_message = "Use ReAct reasoning."
        tools = react_tools
    run_conversation(client, system_message)