from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


def stream_text_completion(
    prompt, model="gpt-4o-mini", max_tokens=1024, temperature=0.7
):
    """
    Stream text completion response from OpenAI API
    """
    try:
        # Create streaming completion
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,  # Enable streaming
        )

        # Initialize response collector
        full_response = ""

        print("Assistant: ", end="", flush=True)

        # Process streaming chunks
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content

        print()  # Newline after completion
        return full_response

    except Exception as e:
        print(f"Error during streaming: {e}")
        return None


def interactive_chat():
    """
    Interactive CLI chat interface with streaming
    """
    print("=" * 60)
    print("OpenAI Text Streaming Chat Interface")
    print("=" * 60)
    print("Type your messages and see responses stream in real-time!")
    print("Commands: 'exit' to quit, 'clear' to clear screen, 'help' for options")
    print("=" * 60)

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Handle commands
            if user_input.lower() == "exit":
                print("Goodbye! Thanks for using the streaming chat!")
                break
            elif user_input.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                print("=" * 60)
                print("OpenAI Text Streaming Chat Interface")
                print("=" * 60)
                continue
            elif user_input.lower() == "help":
                print("\n Available Commands:")
                print("  - Just type your message to chat")
                print("  - 'exit' - Quit the application")
                print("  - 'clear' - Clear the screen")
                print("  - 'help' - Show this help message")
                continue
            elif not user_input:
                print("Please enter a message or use 'help' for commands.")
                continue

            # Stream the response
            response = stream_text_completion(user_input)

            if response is None:
                print(" Failed to get response. Please try again.")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again or type 'exit' to quit.")


def demo_streaming():
    """
    Demo function showing different streaming examples
    """
    print("Streaming Demo Examples")
    print("=" * 40)

    # Example 1: Creative writing
    print("\nExample 1: Creative Writing")
    prompt1 = "Write a short story about a robot learning to paint"
    stream_text_completion(prompt1, temperature=0.8)

    # Example 2: Code explanation
    print("\nExample 2: Code Explanation")
    prompt2 = "Explain what this Python code does: def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
    stream_text_completion(prompt2, temperature=0.3)

    # Example 3: Math problem
    print("\nExample 3: Math Problem")
    prompt3 = "Solve this math problem step by step: If a train travels 120 km in 2 hours, what is its speed in km/h?"
    stream_text_completion(prompt3, temperature=0.1)


if __name__ == "__main__":
    import sys

    # Check if demo mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_streaming()
    else:
        # Start interactive chat
        interactive_chat()
