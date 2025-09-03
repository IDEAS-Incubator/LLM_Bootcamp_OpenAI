"""
LLM Bootcamp OpenAI Demo - Models Listing
GET /v1/models - List models and metadata
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def list_models():
    """List all available models and their metadata"""
    try:
        models = client.models.list()

        print("=== Available OpenAI Models ===")
        print(f"Total models found: {len(models.data)}")
        print()

        for model in models.data:
            print(f"Model ID: {model.id}")
            print(f"Object: {model.object}")
            print(f"Created: {model.created}")
            print(f"Owned by: {model.owned_by}")
            print("-" * 50)

        return models

    except Exception as e:
        print(f"Error listing models: {e}")
        return None


def get_model_details(model_id):
    """Get detailed information about a specific model"""
    try:
        model = client.models.retrieve(model_id)

        print(f"=== Model Details for {model_id} ===")
        print(f"Model ID: {model.id}")
        print(f"Object: {model.object}")
        print(f"Created: {model.created}")
        print(f"Owned by: {model.owned_by}")

        return model

    except Exception as e:
        print(f"Error retrieving model {model_id}: {e}")
        return None


if __name__ == "__main__":
    # List all models
    models = list_models()

    # Get details for specific models
    print("\n" + "=" * 60 + "\n")

    # Get details for GPT-4
    gpt4_model = get_model_details("gpt-4")

    print("\n" + "=" * 60 + "\n")

    # Get details for GPT-3.5-turbo
    gpt35_model = get_model_details("gpt-3.5-turbo")
