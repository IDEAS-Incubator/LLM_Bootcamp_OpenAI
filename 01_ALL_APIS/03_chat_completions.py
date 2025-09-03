"""
LLM Bootcamp OpenAI Demo - Chat Completions
POST /v1/chat/completions - Chat-style completion (multi-turn)
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def basic_chat(message, model="gpt-3.5-turbo"):
    """Basic chat completion"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=150,
            temperature=0.7,
        )

        print(f"=== Basic Chat ===")
        print(f"User: {message}")
        print(f"Assistant: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in basic chat: {e}")
        return None


def multi_turn_conversation(messages, model="gpt-3.5-turbo"):
    """Multi-turn conversation"""
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=200, temperature=0.7
        )

        print(f"=== Multi-turn Conversation ===")
        print("Conversation History:")
        for msg in messages:
            print(f"{msg['role'].title()}: {msg['content']}")
        print(f"Assistant: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in multi-turn conversation: {e}")
        return None


def system_prompt_chat(system_prompt, user_message, model="gpt-3.5-turbo"):
    """Chat with system prompt to define behavior"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=200,
            temperature=0.7,
        )

        print(f"=== System Prompt Chat ===")
        print(f"System: {system_prompt}")
        print(f"User: {user_message}")
        print(f"Assistant: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in system prompt chat: {e}")
        return None


def streaming_chat(message, model="gpt-3.5-turbo"):
    """Streaming chat completion"""
    try:
        print(f"=== Streaming Chat ===")
        print(f"User: {message}")
        print("Assistant: ", end="", flush=True)

        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=200,
            temperature=0.7,
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content

        print("\n" + "=" * 60)

        return full_response

    except Exception as e:
        print(f"Error in streaming chat: {e}")
        return None


if __name__ == "__main__":
    # Basic chat
    basic_chat("Hello! How are you today?")

    print("\n" + "=" * 60 + "\n")

    # Multi-turn conversation
    conversation = [
        {"role": "user", "content": "I want to learn Python programming."},
        {
            "role": "assistant",
            "content": "Great! Python is an excellent programming language to learn. What would you like to know about it?",
        },
        {"role": "user", "content": "What are the best resources for beginners?"},
    ]
    multi_turn_conversation(conversation)

    print("\n" + "=" * 60 + "\n")

    # System prompt chat
    system_prompt = "You are a helpful coding assistant. Always provide code examples when explaining programming concepts."
    system_prompt_chat(system_prompt, "Explain what a function is in programming.")

    print("\n" + "=" * 60 + "\n")

    print("\n" + "=" * 60 + "\n")

    # Streaming chat
    streaming_chat("Tell me a short story about artificial intelligence.")
