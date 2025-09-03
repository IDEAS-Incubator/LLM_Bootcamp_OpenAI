from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from enum import Enum
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)


class SentimentType(str, Enum):
    """Enumeration for sentiment types"""

    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class SentimentAnalysis(BaseModel):
    """Pydantic model for structured sentiment analysis response"""

    sentiment: SentimentType = Field(description="The classified sentiment")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
    explanation: str = Field(
        description="Brief explanation of the sentiment classification"
    )
    keywords: list[str] = Field(
        description="Key words/phrases that influenced the classification"
    )
    intensity: str = Field(
        description="Intensity level: Very Low, Low, Medium, High, Very High"
    )


def analyze_sentiment_structured(text: str) -> SentimentAnalysis:
    """
    Analyzes the sentiment of the provided text using OpenAI API with structured output.

    Args:
        text (str): The text to analyze.

    Returns:
        SentimentAnalysis: Structured sentiment analysis result.
    """
    try:
        # Use response_format with Pydantic model for structured output
        completion = client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a sentiment analysis expert. Analyze the sentiment of text and provide detailed classification.

Guidelines for classification:
- Positive: Expresses happiness, satisfaction, approval, or positive emotions
- Negative: Expresses anger, frustration, disappointment, or negative emotions  
- Neutral: Factual, objective, or balanced statements without strong emotional content

Consider context, tone, and emotional indicators when classifying sentiment.
Provide confidence scores between 0.0 and 1.0, and identify key words that influenced your decision.""",
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this text: {text}",
                },
            ],
            response_format=SentimentAnalysis,
            max_tokens=300,
            temperature=0.1,
        )

        # Return the parsed sentiment analysis
        return completion.choices[0].message.parsed

    except Exception as e:
        # Return a default neutral response on error
        return SentimentAnalysis(
            sentiment=SentimentType.NEUTRAL,
            confidence=0.0,
            explanation=f"Error during analysis: {str(e)}",
            keywords=[],
            intensity="Very Low",
        )


def analyze_sentiment_batch(texts: list[str]) -> list[SentimentAnalysis]:
    """
    Analyze sentiment for multiple texts in batch.

    Args:
        texts (list[str]): List of texts to analyze.

    Returns:
        list[SentimentAnalysis]: List of sentiment analysis results.
    """
    results = []
    for text in texts:
        result = analyze_sentiment_structured(text)
        results.append(result)
    return results


def print_sentiment_analysis(analysis: SentimentAnalysis, text: str = ""):
    """
    Print sentiment analysis results in a formatted way.

    Args:
        analysis (SentimentAnalysis): The sentiment analysis result.
        text (str): The original text (optional).
    """
    if text:
        print(f"Text: {text}")

    # Sentiment labels
    sentiment_labels = {
        SentimentType.POSITIVE: "[Positive]",
        SentimentType.NEGATIVE: "[Negative]",
        SentimentType.NEUTRAL: "[Neutral]",
    }

    label = sentiment_labels.get(analysis.sentiment, "[Unknown]")

    print(f"{label} Sentiment: {analysis.sentiment}")
    print(f"Confidence: {analysis.confidence:.2%}")
    print(f"Explanation: {analysis.explanation}")
    print(f"Keywords: {', '.join(analysis.keywords)}")
    print(f"Intensity: {analysis.intensity}")
    print("-" * 50)


def interactive_sentiment_demo():
    """
    Interactive demo for sentiment analysis
    """
    print("=" * 60)
    print("Sentiment Analysis with OpenAI Demo")
    print("=" * 60)
    print("1. Single text analysis")
    print("2. Batch analysis (multiple texts)")
    print("3. Demo examples")
    print("4. Exit")
    print("=" * 60)

    while True:
        try:
            choice = input("\nChoose an option (1-4): ").strip()

            if choice == "1":
                # Single text analysis
                print("\nSingle Text Analysis")
                print("-" * 40)

                text = input("Enter text to analyze: ").strip()
                if text:
                    analysis = analyze_sentiment_structured(text)
                    print_sentiment_analysis(analysis, text)
                else:
                    print("Please enter some text.")

            elif choice == "2":
                # Batch analysis
                print("\nBatch Analysis")
                print("-" * 40)

                texts = []
                print("Enter texts (one per line, empty line to finish):")
                while True:
                    text = input().strip()
                    if not text:
                        break
                    texts.append(text)

                if texts:
                    print(f"\nAnalyzing {len(texts)} texts...")
                    results = analyze_sentiment_batch(texts)

                    for i, (text, analysis) in enumerate(zip(texts, results), 1):
                        print(f"\n--- Text {i} ---")
                        print_sentiment_analysis(analysis, text)
                else:
                    print("No texts entered.")

            elif choice == "3":
                # Demo examples
                print("\nDemo Examples")
                print("-" * 40)

                demo_texts = [
                    "I love how user-friendly and powerful OpenAI's tools are!",
                    "Your software does not work at all and I'm very frustrated.",
                    "The weather today is sunny with a temperature of 25 degrees Celsius.",
                    "This product exceeded my expectations and I'm thrilled with the results!",
                    "I'm extremely disappointed with the poor customer service I received.",
                    "The meeting will be held tomorrow at 2 PM in the conference room.",
                ]

                for i, text in enumerate(demo_texts, 1):
                    print(f"\n--- Example {i} ---")
                    analysis = analyze_sentiment_structured(text)
                    print_sentiment_analysis(analysis, text)
                    input("Press Enter to continue...")

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1-4.")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    # Run interactive demo
    interactive_sentiment_demo()
