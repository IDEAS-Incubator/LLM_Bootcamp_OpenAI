"""
LLM Bootcamp OpenAI Demo - Realtime Interaction
POST /v1/realtime - Low-latency multimodal interaction
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def basic_realtime_interaction(prompt, model="gpt-4o"):
    """Basic realtime interaction"""
    try:
        response = client.realtime.create(model=model, input=prompt)

        print(f"=== Basic Realtime Interaction ===")
        print(f"Prompt: {prompt}")
        print(f"Model: {model}")
        print(f"Response: {response.output[0].content[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in basic realtime interaction: {e}")
        return None


def realtime_with_tools(prompt, tools, model="gpt-4o"):
    """Realtime interaction with tool usage"""
    try:
        response = client.realtime.create(model=model, input=prompt, tools=tools)

        print(f"=== Realtime with Tools ===")
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
        print(f"Error in realtime with tools: {e}")
        return None


def realtime_conversation(messages, model="gpt-4o"):
    """Multi-turn realtime conversation"""
    try:
        response = client.realtime.create(model=model, input=messages)

        print(f"=== Realtime Conversation ===")
        print(f"Model: {model}")
        print("Conversation:")
        for message in messages:
            print(f"- {message}")
        print(f"Assistant: {response.output[0].content[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in realtime conversation: {e}")
        return None


def realtime_weather_example():
    """Example using weather tool in realtime"""
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

    prompt = "What's the weather like in Tokyo right now?"

    return realtime_with_tools(prompt, tools)


def realtime_calculator_example():
    """Example using calculator tool in realtime"""
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
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    prompt = "Calculate 42 * 17 + 89"

    return realtime_with_tools(prompt, tools)


def realtime_multimodal_example():
    """Example of multimodal realtime interaction"""
    print("=== Realtime Multimodal Example ===")
    print("Note: This example demonstrates the concept of multimodal interaction.")
    print("In a real implementation, you would include images, audio, or other media.")

    # Example conversation that could include multiple modalities
    conversation = [
        "I have an image of a cat. Can you describe what you see?",
        "The image shows a fluffy orange cat sitting on a windowsill.",
        "What breed do you think it is?",
        "Based on the image, it appears to be a domestic shorthair with orange tabby markings.",
    ]

    return realtime_conversation(conversation)


def latency_comparison():
    """Compare latency between regular and realtime APIs"""
    print("=== Latency Comparison ===")

    test_prompt = "What is 2 + 2?"

    # Test regular chat completion
    print("Testing regular chat completion...")
    start_time = time.time()
    try:
        regular_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=50,
        )
        regular_time = time.time() - start_time
        print(f"Regular API response time: {regular_time:.3f} seconds")
    except Exception as e:
        print(f"Error testing regular API: {e}")
        regular_time = None

    # Test realtime
    print("Testing realtime API...")
    start_time = time.time()
    try:
        realtime_response = client.realtime.create(model="gpt-4o", input=test_prompt)
        realtime_time = time.time() - start_time
        print(f"Realtime API response time: {realtime_time:.3f} seconds")
    except Exception as e:
        print(f"Error testing realtime API: {e}")
        realtime_time = None

    if regular_time and realtime_time:
        if realtime_time < regular_time:
            improvement = ((regular_time - realtime_time) / regular_time) * 100
            print(f"Realtime API is {improvement:.1f}% faster")
        else:
            slowdown = ((realtime_time - regular_time) / regular_time) * 100
            print(f"Realtime API is {slowdown:.1f}% slower")


def realtime_examples():
    """Run various realtime examples"""
    print("=== Realtime Interaction Examples ===")

    # Example 1: Basic realtime
    print("\n1. Basic Realtime Interaction")
    basic_realtime_interaction("Hello! How are you today?")

    # Example 2: Weather tool
    print("\n2. Realtime Weather Tool")
    realtime_weather_example()

    # Example 3: Calculator tool
    print("\n3. Realtime Calculator Tool")
    realtime_calculator_example()

    # Example 4: Conversation
    print("\n4. Realtime Conversation")
    conversation = [
        "I'm planning a trip to Paris.",
        "What should I know about the weather there?",
        "Can you recommend some activities?",
    ]
    realtime_conversation(conversation)

    # Example 5: Multimodal
    print("\n5. Realtime Multimodal Example")
    realtime_multimodal_example()


def realtime_guidelines():
    """Show realtime interaction guidelines"""
    print("=== Realtime Interaction Guidelines ===")

    guidelines = [
        "Realtime API Benefits:",
        "- Lower latency for faster responses",
        "- Optimized for interactive applications",
        "- Better for real-time chat and conversations",
        "- Reduced waiting time for users",
        "",
        "Best Use Cases:",
        "- Live chat applications",
        "- Interactive AI assistants",
        "- Real-time customer support",
        "- Gaming and entertainment",
        "- Educational applications",
        "",
        "Considerations:",
        "- May have different rate limits",
        "- Optimized for shorter, more frequent interactions",
        "- Best for conversational contexts",
        "- Consider cost implications for high-volume usage",
    ]

    for guideline in guidelines:
        print(guideline)


if __name__ == "__main__":
    # Show guidelines
    realtime_guidelines()

    print("\n" + "=" * 60 + "\n")

    # Run examples
    realtime_examples()

    print("\n" + "=" * 60 + "\n")

    # Latency comparison
    latency_comparison()

    print("\n" + "=" * 60 + "\n")

    # Interactive example
    print("=== Interactive Realtime Test ===")
    print("Enter a prompt for realtime interaction (or press Enter to skip):")
    user_input = input("> ")

    if user_input.strip():
        basic_realtime_interaction(user_input)
    else:
        print("Skipped interactive test.")

    print("\n" + "=" * 60 + "\n")
    print(
        "Realtime interactions provide low-latency responses for interactive applications."
    )
    print(
        "Perfect for chat applications, live assistants, and real-time user experiences."
    )
