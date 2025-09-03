"""
LLM Bootcamp OpenAI Demo - Assistant Responses
POST /v1/responses - Tool-augmented chat + agent functionality
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def basic_assistant_response(prompt, model="gpt-4o"):
    """Basic assistant response without tools"""
    try:
        response = client.responses.create(model=model, input=prompt)

        print(f"=== Basic Assistant Response ===")
        print(f"Prompt: {prompt}")
        print(f"Model: {model}")
        print(f"Response: {response.output[0].content[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in basic assistant response: {e}")
        return None


def assistant_with_tools(prompt, tools, model="gpt-4o"):
    """Assistant response with tool usage"""
    try:
        response = client.responses.create(model=model, input=prompt, tools=tools)

        print(f"=== Assistant with Tools ===")
        print(f"Prompt: {prompt}")
        print(f"Model: {model}")
        print(f"Response: {response.output[0].content[0].text}")

        # Check if tools were used
        if hasattr(response.output[0].content[0], "tool_calls"):
            tool_calls = response.output[0].content[0].tool_calls
            if tool_calls:
                print(f"Tools used: {len(tool_calls)}")
                for i, tool_call in enumerate(tool_calls):
                    print(f"Tool {i+1}: {tool_call.name}")
                    print(f"Arguments: {tool_call.args}")

        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in assistant with tools: {e}")
        return None


def weather_tool_example():
    """Example using a weather tool"""
    tools = [
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
                            "description": "The city and state, e.g. San Francisco, CA",
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
        }
    ]

    prompt = "What's the weather like in New York City?"

    return assistant_with_tools(prompt, tools)


def calculator_tool_example():
    """Example using a calculator tool"""
    tools = [
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
                            "description": "The mathematical expression to evaluate, e.g. '2 + 2 * 3'",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    prompt = "What is 15 * 23 + 7?"

    return assistant_with_tools(prompt, tools)


def multi_tool_example():
    """Example using multiple tools"""
    tools = [
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
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
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
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for current information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"}
                    },
                    "required": ["query"],
                },
            },
        },
    ]

    prompt = "What's the weather in London and what's 25 * 4?"

    return assistant_with_tools(prompt, tools)


def assistant_conversation(messages, model="gpt-4o"):
    """Multi-turn conversation with assistant"""
    try:
        response = client.responses.create(model=model, input=messages)

        print(f"=== Assistant Conversation ===")
        print(f"Model: {model}")
        print("Conversation:")
        for message in messages:
            print(f"- {message}")
        print(f"Assistant: {response.output[0].content[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in assistant conversation: {e}")
        return None


def assistant_with_system_prompt(prompt, system_prompt, model="gpt-4o"):
    """Assistant with system prompt to define behavior"""
    try:
        # Create input with system message
        input_data = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = client.responses.create(model=model, input=input_data)

        print(f"=== Assistant with System Prompt ===")
        print(f"System: {system_prompt}")
        print(f"User: {prompt}")
        print(f"Assistant: {response.output[0].content[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in assistant with system prompt: {e}")
        return None


def assistant_examples():
    """Run various assistant examples"""
    print("=== Assistant Response Examples ===")

    # Example 1: Basic response
    print("\n1. Basic Assistant Response")
    basic_assistant_response("Explain quantum computing in simple terms.")

    # Example 2: Weather tool
    print("\n2. Weather Tool Example")
    weather_tool_example()

    # Example 3: Calculator tool
    print("\n3. Calculator Tool Example")
    calculator_tool_example()

    # Example 4: Multi-tool example
    print("\n4. Multi-Tool Example")
    multi_tool_example()

    # Example 5: Conversation
    print("\n5. Assistant Conversation")
    conversation = [
        "I want to learn about machine learning.",
        "What are the best resources for beginners?",
        "Can you recommend some online courses?",
    ]
    assistant_conversation(conversation)

    # Example 6: System prompt
    print("\n6. Assistant with System Prompt")
    system_prompt = "You are a helpful coding assistant. Always provide code examples when explaining programming concepts."
    assistant_with_system_prompt(
        "Explain what a function is in programming.", system_prompt
    )


def tool_definitions():
    """Show common tool definitions"""
    print("=== Common Tool Definitions ===")

    tools = {
        "weather": {
            "name": "get_weather",
            "description": "Get current weather information",
            "parameters": {"location": "string", "unit": "celsius|fahrenheit"},
        },
        "calculator": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {"expression": "string"},
        },
        "search": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {"query": "string"},
        },
        "database": {
            "name": "query_database",
            "description": "Query a database",
            "parameters": {"query": "string", "table": "string"},
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
    assistant_examples()

    print("\n" + "=" * 60 + "\n")

    # Interactive example
    print("=== Interactive Assistant Test ===")
    print("Enter a prompt for the assistant (or press Enter to skip):")
    user_input = input("> ")

    if user_input.strip():
        basic_assistant_response(user_input)
    else:
        print("Skipped interactive test.")

    print("\n" + "=" * 60 + "\n")
    print("Assistant responses provide tool-augmented chat capabilities.")
    print(
        "Tools allow the assistant to perform specific actions and access external data."
    )
