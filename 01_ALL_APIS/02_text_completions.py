"""
LLM Bootcamp OpenAI Demo - Text Completions
POST /v1/completions - Text completion (single-prompt)
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def basic_completion(prompt, model="gpt-3.5-turbo-instruct"):
    """Basic text completion"""
    try:
        response = client.completions.create(
            model=model, prompt=prompt, max_tokens=100, temperature=0.7
        )

        print(f"=== Basic Completion ===")
        print(f"Prompt: {prompt}")
        print(f"Response: {response.choices[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in basic completion: {e}")
        return None


def creative_writing(prompt, model="gpt-3.5-turbo-instruct"):
    """Creative writing with higher temperature"""
    try:
        response = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=200,
            temperature=0.9,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1,
        )

        print(f"=== Creative Writing ===")
        print(f"Prompt: {prompt}")
        print(f"Response: {response.choices[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in creative writing: {e}")
        return None


def code_completion(code_prompt, model="gpt-3.5-turbo-instruct"):
    """Code completion with specific parameters"""
    try:
        response = client.completions.create(
            model=model,
            prompt=code_prompt,
            max_tokens=150,
            temperature=0.1,  # Lower temperature for more deterministic code
            stop=["\n\n", "```"],  # Stop at double newlines or code blocks
        )

        print(f"=== Code Completion ===")
        print(f"Code Prompt: {code_prompt}")
        print(f"Generated Code: {response.choices[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in code completion: {e}")
        return None


def structured_completion(prompt, model="gpt-3.5-turbo-instruct"):
    """Structured completion with specific format"""
    try:
        structured_prompt = f"""
{prompt}

Please provide your response in the following format:
- Summary: [brief summary]
- Key Points: [list of key points]
- Conclusion: [conclusion]
"""

        response = client.completions.create(
            model=model, prompt=structured_prompt, max_tokens=300, temperature=0.5
        )

        print(f"=== Structured Completion ===")
        print(f"Original Prompt: {prompt}")
        print(f"Structured Response: {response.choices[0].text}")
        print(f"Usage: {response.usage}")

        return response

    except Exception as e:
        print(f"Error in structured completion: {e}")
        return None


if __name__ == "__main__":
    # Basic completion
    basic_completion("Explain the concept of machine learning in simple terms.")

    print("\n" + "=" * 60 + "\n")

    # Creative writing
    creative_writing("Write a short story about a robot learning to paint.")

    print("\n" + "=" * 60 + "\n")

    # Code completion
    code_completion("def fibonacci(n):\n    if n <= 1:\n        return n\n    return")

    print("\n" + "=" * 60 + "\n")

    # Structured completion
    structured_completion("Discuss the benefits and challenges of renewable energy.")
