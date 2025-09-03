"""
LLM Bootcamp OpenAI Demo - Content Moderation
POST /v1/moderations - Check text against content policy
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def moderate_text(text, model="text-moderation-latest"):
    """Check text against OpenAI's content policy"""
    try:
        response = client.moderations.create(input=text, model=model)

        print(f"=== Content Moderation ===")
        print(f"Text: {text}")
        print(f"Model: {model}")
        print(f"Flagged: {response.results[0].flagged}")

        if response.results[0].flagged:
            print("Categories flagged:")
            categories = response.results[0].categories
            for category, flagged in categories.__dict__.items():
                if flagged:
                    print(f"- {category}: {flagged}")

        print(f"Category scores:")
        scores = response.results[0].category_scores
        for category, score in scores.__dict__.items():
            print(f"- {category}: {score:.4f}")

        return response

    except Exception as e:
        print(f"Error in content moderation: {e}")
        return None


def moderate_multiple_texts(texts, model="text-moderation-latest"):
    """Check multiple texts against content policy"""
    try:
        response = client.moderations.create(input=texts, model=model)

        print(f"=== Multiple Texts Moderation ===")
        print(f"Model: {model}")
        print(f"Number of texts: {len(texts)}")

        for i, result in enumerate(response.results):
            print(f"\nText {i+1}: {texts[i]}")
            print(f"Flagged: {result.flagged}")

            if result.flagged:
                print("Categories flagged:")
                categories = result.categories
                for category, flagged in categories.__dict__.items():
                    if flagged:
                        print(f"- {category}: {flagged}")

        return response

    except Exception as e:
        print(f"Error in multiple texts moderation: {e}")
        return None


def check_specific_categories(text, model="text-moderation-latest"):
    """Check specific categories of concern"""
    try:
        response = client.moderations.create(input=text, model=model)

        print(f"=== Specific Categories Check ===")
        print(f"Text: {text}")
        print(f"Model: {model}")

        categories = response.results[0].categories
        scores = response.results[0].category_scores

        # Define category descriptions
        category_descriptions = {
            "hate": "Content expressing hate or violence against protected groups",
            "hate_threatening": "Content expressing hate with threat of violence",
            "self_harm": "Content promoting self-harm or suicide",
            "sexual": "Content of a sexual nature",
            "sexual_minors": "Content involving minors in sexual contexts",
            "violence": "Content promoting violence",
            "violence_graphic": "Graphic content promoting violence",
        }

        print("\nCategory Analysis:")
        for category, description in category_descriptions.items():
            flagged = getattr(categories, category, False)
            score = getattr(scores, category, 0.0)
            print(
                f"- {category}: {score:.4f} {'🚩' if flagged else '✅'} - {description}"
            )

        return response

    except Exception as e:
        print(f"Error in specific categories check: {e}")
        return None


def moderation_examples():
    """Run various moderation examples"""
    print("=== Content Moderation Examples ===")

    # Example 1: Safe text
    safe_text = "Hello! How are you today? I hope you're having a wonderful day."
    print("\n1. Safe Text Example")
    moderate_text(safe_text)

    # Example 2: Potentially concerning text (educational context)
    concerning_text = "This is a discussion about violence in historical contexts for educational purposes."
    print("\n2. Concerning Text Example (Educational)")
    moderate_text(concerning_text)

    # Example 3: Multiple texts
    multiple_texts = [
        "Have a great day!",
        "This is a test of the moderation system.",
        "Let's discuss programming concepts.",
    ]
    print("\n3. Multiple Texts Example")
    moderate_multiple_texts(multiple_texts)

    # Example 4: Specific categories check
    test_text = "This is a test message for content moderation."
    print("\n4. Specific Categories Check")
    check_specific_categories(test_text)


def moderation_guidelines():
    """Show moderation guidelines and best practices"""
    print("=== Content Moderation Guidelines ===")

    guidelines = [
        "OpenAI's content policy prohibits:",
        "- Hate speech and harassment",
        "- Violence and graphic content",
        "- Self-harm content",
        "- Sexual content involving minors",
        "- Misinformation and disinformation",
        "- Privacy violations",
        "",
        "Best Practices:",
        "- Always moderate user-generated content",
        "- Use appropriate thresholds for your use case",
        "- Consider context when interpreting results",
        "- Implement additional safety measures",
        "- Monitor and update moderation rules regularly",
    ]

    for guideline in guidelines:
        print(guideline)


def threshold_examples():
    """Show how different thresholds affect moderation"""
    print("=== Threshold Examples ===")

    test_texts = [
        "I love this community!",
        "This is a discussion about historical events.",
        "Let's talk about programming and technology.",
    ]

    print("Different moderation thresholds:")
    print("- Low threshold (0.1): More sensitive, flags more content")
    print("- Medium threshold (0.5): Balanced approach")
    print("- High threshold (0.9): Less sensitive, flags only obvious violations")

    print("\nNote: OpenAI's moderation API uses internal thresholds.")
    print("You can implement your own thresholds based on category scores.")


if __name__ == "__main__":
    # Show guidelines
    moderation_guidelines()

    print("\n" + "=" * 60 + "\n")

    # Threshold examples
    threshold_examples()

    print("\n" + "=" * 60 + "\n")

    # Run examples
    moderation_examples()

    print("\n" + "=" * 60 + "\n")

    # Interactive example
    print("=== Interactive Moderation Test ===")
    print("Enter a text to moderate (or press Enter to skip):")
    user_input = input("> ")

    if user_input.strip():
        moderate_text(user_input)
    else:
        print("Skipped interactive test.")

    print("\n" + "=" * 60 + "\n")
    print("Content moderation helps ensure safe and appropriate use of AI systems.")
    print("Always implement moderation in production applications.")
