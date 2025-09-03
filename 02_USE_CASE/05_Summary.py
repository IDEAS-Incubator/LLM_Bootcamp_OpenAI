from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


def summarize_article(article_text):
    try:
        # Define the prompt for summarization
        prompt = (
            "Please summarize the following article in a concise manner:\n\n"
            f"{article_text}\n\n"
            "Summary:"
        )

        # Call OpenAI's text completion endpoint
        response = client.completions.create(
            model="gpt-4o-mini",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150,  # Limit the summary length
            stream=False,
        )

        # Extract and return the summary
        summary = response.choices[0].text.strip()

        return summary

    except Exception as e:  # Catch generic exceptions
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Example article text
    article_text = """
    OpenAI has developed a suite of powerful AI models that are capable of understanding and generating human-like text. 
    These models have been applied to a variety of tasks, such as language translation, summarization, and content creation. 
    The advancements in AI have sparked discussions about ethical use, accessibility, and the potential impact on various industries.
    """

    # Generate and print the summary
    summary = summarize_article(article_text)
    print("Summary:")
    print(summary)
