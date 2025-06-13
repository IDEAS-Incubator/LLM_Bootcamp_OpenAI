from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

if not my_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")


# Initialize OpenAI client
client = OpenAI(api_key=my_key)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn.",
        }
    ],
)

print(response.choices[0].message.content)
