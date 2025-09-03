"""
LLM Bootcamp OpenAI Demo - Assistant Responses with Real APIs
POST /v1/chat/completions - Tool-augmented chat with weather and calculator APIs
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import requests
import math
import re

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_coordinates(location):
    """Get coordinates for a location using free geocoding API"""
    try:
        # Using Nominatim (OpenStreetMap) geocoding API - free and no API key required
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location, "format": "json", "limit": 1, "addressdetails": 1}

        headers = {"User-Agent": "WeatherAssistant/1.0"}  # Required by Nominatim

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if response.status_code == 200 and data:
            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])
            display_name = result.get("display_name", location)

            return {
                "location": location,
                "latitude": lat,
                "longitude": lon,
                "display_name": display_name,
                "success": True,
            }
        else:
            return {
                "location": location,
                "error": "Location not found",
                "success": False,
            }

    except Exception as e:
        return {
            "location": location,
            "error": f"Geocoding error: {str(e)}",
            "success": False,
        }


def get_weather(location, unit="celsius"):
    """Get real weather data using Open-Meteo API (no API key required)"""
    try:
        # First get coordinates for the location
        coords_result = get_coordinates(location)

        if not coords_result["success"]:
            return {"error": f"Could not find coordinates for {location}"}

        lat = coords_result["latitude"]
        lon = coords_result["longitude"]
        display_name = coords_result["display_name"]

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and "current" in data:
            current = data["current"]
            temp_c = current["temperature_2m"]
            temp_f = (temp_c * 9 / 5) + 32
            humidity = current["relative_humidity_2m"]
            wind_speed = current["wind_speed_10m"]

            weather_codes = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Foggy",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                95: "Thunderstorm",
            }

            weather_desc = weather_codes.get(current["weather_code"], "Unknown")

            if unit.lower() == "fahrenheit":
                temperature = f"{temp_f:.1f}°F"
            else:
                temperature = f"{temp_c:.1f}°C"

            return {
                "location": display_name,
                "coordinates": f"{lat:.4f}, {lon:.4f}",
                "temperature": temperature,
                "description": weather_desc,
                "humidity": f"{humidity}%",
                "wind_speed": f"{wind_speed} km/h",
            }
        else:
            return {"error": "Unable to fetch weather data"}
    except Exception as e:
        return {"error": f"Error fetching weather: {str(e)}"}


def calculate(expression):
    """Perform mathematical calculations safely"""
    try:
        # Remove any potentially dangerous characters and validate
        expression = expression.strip()

        # Only allow safe mathematical operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}

        # Check for potentially dangerous operations
        dangerous_patterns = ["eval", "exec", "import", "__", "open", "file"]
        if any(pattern in expression.lower() for pattern in dangerous_patterns):
            return {"error": "Potentially dangerous operation detected"}

        # Evaluate the expression
        result = eval(expression)

        # Check if result is a number
        if isinstance(result, (int, float)):
            return {"result": result, "expression": expression}
        else:
            return {"error": "Expression must evaluate to a number"}

    except ZeroDivisionError:
        return {"error": "Division by zero"}
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}


def assistant_with_tools(prompt, model="gpt-4o"):
    """Assistant response with real tool usage"""
    try:
        # Define the tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_coordinates",
                    "description": "Get coordinates (latitude and longitude) for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location name, e.g. New York, London, Tokyo, San Francisco",
                            }
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name, e.g. New York, London, Tokyo",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate, e.g. '2 + 2 * 3', '15 * 23 + 7'",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            },
        ]

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            tool_choice="auto",
        )

        print(f"=== Assistant with Real Tools ===")
        print(f"Prompt: {prompt}")
        print(f"Model: {model}")

        # Check if tools were used
        if response.choices[0].message.tool_calls:
            tool_calls = response.choices[0].message.tool_calls
            print(f"Tools used: {len(tool_calls)}")

            # Execute the tools and get results
            tool_results = []
            for i, tool_call in enumerate(tool_calls):
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"Tool {i+1}: {tool_name}")
                print(f"Arguments: {tool_args}")

                # Execute the tool
                if tool_name == "get_coordinates":
                    result = get_coordinates(**tool_args)
                elif tool_name == "get_weather":
                    result = get_weather(**tool_args)
                elif tool_name == "calculate":
                    result = calculate(**tool_args)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(result),
                    }
                )

                print(f"Result: {result}")

            # Send the tool results back to the assistant
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": None, "tool_calls": tool_calls},
            ]
            messages.extend(tool_results)

            final_response = client.chat.completions.create(
                model=model, messages=messages
            )

            print(f"Final Response: {final_response.choices[0].message.content}")
            print(f"Usage: {final_response.usage}")

            return final_response
        else:
            print(f"Response: {response.choices[0].message.content}")
            print(f"Usage: {response.usage}")
            return response

    except Exception as e:
        print(f"Error in assistant with tools: {e}")
        return None


def coordinates_example():
    """Example using coordinates tool"""
    prompt = "What are the coordinates for San Francisco?"
    return assistant_with_tools(prompt)


def weather_example():
    """Example using weather tool"""
    prompt = "What's the weather like in Tokyo?"
    return assistant_with_tools(prompt)


def calculator_example():
    """Example using calculator tool"""
    prompt = "What is 15 * 23 + 7?"
    return assistant_with_tools(prompt)


def combined_example():
    """Example using multiple tools"""
    prompt = "What are the coordinates for Paris and what's the weather there?"
    return assistant_with_tools(prompt)


def interactive_assistant():
    """Interactive assistant with real tools"""
    print("=== Interactive Assistant with Real Tools ===")
    print("I can help you with:")
    print("- Getting coordinates for any location")
    print("- Weather information for any city")
    print("- Mathematical calculations")
    print("Examples:")
    print("- 'What are the coordinates for Tokyo?'")
    print("- 'What's the weather in Paris?'")
    print("- 'Calculate 15 * 23 + 7'")
    print("- 'What are the coordinates for New York and what's the weather there?'")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if user_input:
            print("\n" + "=" * 50)
            assistant_with_tools(user_input)
            print("=" * 50)


def tool_definitions():
    """Show tool definitions"""
    print("=== Available Tools ===")

    tools = {
        "coordinates": {
            "name": "get_coordinates",
            "description": "Get coordinates (latitude/longitude) for any location using free geocoding API",
            "parameters": {"location": "string (location name)"},
        },
        "weather": {
            "name": "get_weather",
            "description": "Get current weather information using free weather API",
            "parameters": {
                "location": "string (city name)",
                "unit": "celsius|fahrenheit (optional)",
            },
        },
        "calculator": {
            "name": "calculate",
            "description": "Perform mathematical calculations safely",
            "parameters": {"expression": "string (math expression)"},
        },
    }

    for tool_name, tool_def in tools.items():
        print(f"\n{tool_name.title()} Tool:")
        print(f"- Name: {tool_def['name']}")
        print(f"- Description: {tool_def['description']}")
        print(f"- Parameters: {tool_def['parameters']}")


if __name__ == "__main__":
    # Show tool definitions
    tool_definitions()

    print("\n" + "=" * 60 + "\n")

    # Run examples
    print("=== Tool Examples ===")

    print("\n1. Coordinates Example")
    coordinates_example()

    print("\n2. Weather Example")
    weather_example()

    print("\n3. Calculator Example")
    calculator_example()

    print("\n4. Combined Example")
    combined_example()

    print("\n" + "=" * 60 + "\n")

    # Interactive mode
    interactive_assistant()

    print("\n" + "=" * 60 + "\n")
    print(
        "This assistant uses real APIs for geocoding, weather data, and safe mathematical calculations."
    )
    print(
        "Geocoding data provided by Nominatim (OpenStreetMap) - free, no API key required."
    )
    print("Weather data provided by Open-Meteo API - free, no API key required.")
