from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


def translate_text(text, target_language):
    """
    Translates the given text into the target language using OpenAI API.

    Args:
        text (str): The text to translate.
        target_language (str): The language to translate into (e.g., "French", "Spanish").

    Returns:
        str: Translated text.
    """
    try:
        # Define the translation prompt
        prompt = (
            f"Translate the following text into {target_language}:\n\n"
            f"{text}\n\n"
            f"Translation in {target_language}:"
        )

        # in case the string is too long
        # length = text.len()

        # Call OpenAI's completion endpoint
        response = client.completions.create(
            model="gpt-4o-mini",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.1,
        )
        translation = response.choices[0].text.strip()

        return translation

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Example usage
    original_text = (
        "OpenAI provides tools to make AI more accessible and useful for everyone."
    )
    target_language = "French"

    # Get the translation
    translated_text = translate_text(original_text, target_language)
    print(f"Original Text: {original_text}")
    print(f"Translated Text ({target_language}): {translated_text}")
