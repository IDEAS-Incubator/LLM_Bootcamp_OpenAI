from openai import OpenAI
from dotenv import load_dotenv
import os

# Initialize chat history
chat_history = []

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


# Function to send a message and maintain chat history
def send_message(user_input):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})

    # Add system role message
    system_message = {"role": "system", "content": "you are a helpful data scientist interview assistant."}

    # Combine messages for the API call
    messages = [system_message] + chat_history

    # Call OpenAI API for chat completion with streaming enabled
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=True,  # Enable streaming
    )

    # Initialize an empty string to collect the assistant's response
    assistant_response = ""

    # Stream and process the response chunks
    for chunk in chat_completion:
        # if "choices" in chunk and len(chunk["choices"]) > 0:
        if "choices" in chunk and len(chunk["choices"]) > 0:
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content", "")
            print(content, end="", flush=True)  # Print the streamed content in real-time
            assistant_response += content

    print()  # Print a newline after the streaming is complete

    # Append the assistant's response to the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response


# Chat loop
def chat_cli():
    print("Welcome to Data Scientist Interview Assistant. Ask your question here or type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        response = send_message(user_input)
        print(f"Assistant: {response}\n")


# Run the chat loop if this script is run directly
if __name__ == "__main__":
    chat_cli()
