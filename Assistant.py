from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(
    api_key=my_key
)


def chat_with_assistant():
    print("Assistant: Hello! How can I assist you today? (type 'exit' to quit)")
    conversation = []  # Keeps track of the conversation context

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        # Append the user's message to the conversation
        conversation.append({"role": "user", "content": user_input})

        try:
            # Get the assistant's response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            # Extract the assistant's message
            assistant_message = response.choices[0].message.content
            print(f"Assistant: {assistant_message}")

            # Append the assistant's message to the conversation
            conversation.append({"role": "assistant", "content": assistant_message})

        except client.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    chat_with_assistant()
