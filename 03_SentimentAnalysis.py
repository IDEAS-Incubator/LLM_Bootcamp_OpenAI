from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text using OpenAI API.

    Args:
        text (str): The text to analyze.

    Returns:
        str: Sentiment result (Positive, Negative, Neutral).
    """
    try:
        # Define the system and user messages for sentiment analysis
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that classifies sentiment as Positive, Negative, or Neutral.",
            },
            {
                "role": "user",
                "content": f"Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral:\n\nText: {text}\n\nSentiment:",
            },
        ]

        # Call OpenAI's chat completion endpoint
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=10,  # Short response for classification
            temperature=0,  # Ensure deterministic output
        )

        # Extract and return the sentiment result
        sentiment = response.choices[0].message.content.strip()
        return sentiment

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Example usage
    # example_text = "I love how user-friendly and powerful OpenAI's tools are!"
    example_text = "Your software does not work at all."
    # Analyze the sentiment
    sentiment_result = analyze_sentiment(example_text)
    print(f"Text: {example_text}")
    print(f"Sentiment: {sentiment_result}")
