"""
LLM Bootcamp OpenAI Demo - Embeddings
POST /v1/embeddings - Generate vector embeddings
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def create_embeddings(texts, model="text-embedding-ada-002"):
    """Create embeddings for a list of texts"""
    try:
        response = client.embeddings.create(model=model, input=texts)

        print(f"=== Embeddings Created ===")
        print(f"Model: {model}")
        print(f"Number of texts: {len(texts)}")
        print(f"Embedding dimensions: {len(response.data[0].embedding)}")
        print(f"Usage: {response.usage}")

        return [data.embedding for data in response.data]

    except Exception as e:
        print(f"Error creating embeddings: {e}")
        return None


def single_text_embedding(text, model="text-embedding-ada-002"):
    """Create embedding for a single text"""
    try:
        response = client.embeddings.create(model=model, input=text)

        print(f"=== Single Text Embedding ===")
        print(f"Text: {text}")
        print(f"Model: {model}")
        print(f"Embedding dimensions: {len(response.data[0].embedding)}")
        print(f"First 10 values: {response.data[0].embedding[:10]}")
        print(f"Usage: {response.usage}")

        return response.data[0].embedding

    except Exception as e:
        print(f"Error creating single embedding: {e}")
        return None


def semantic_similarity(text1, text2, model="text-embedding-ada-002"):
    """Calculate semantic similarity between two texts"""
    try:
        # Create embeddings for both texts
        response = client.embeddings.create(model=model, input=[text1, text2])

        embedding1 = response.data[0].embedding
        embedding2 = response.data[1].embedding

        # Calculate cosine similarity
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]

        print(f"=== Semantic Similarity ===")
        print(f"Text 1: {text1}")
        print(f"Text 2: {text2}")
        print(f"Similarity Score: {similarity:.4f}")
        print(f"Usage: {response.usage}")

        return similarity

    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return None


def text_classification_example(model="text-embedding-ada-002"):
    """Example of using embeddings for text classification"""
    try:
        # Sample texts for different categories
        categories = {
            "technology": [
                "Artificial intelligence is transforming industries",
                "Machine learning algorithms are becoming more sophisticated",
                "The latest smartphone features advanced AI capabilities",
            ],
            "sports": [
                "The team won the championship game",
                "Athletes train hard to improve performance",
                "The match was intense and exciting",
            ],
            "food": [
                "This restaurant serves delicious Italian cuisine",
                "The chef prepared a gourmet meal",
                "Fresh ingredients make all the difference",
            ],
        }

        # Create embeddings for all texts
        all_texts = []
        text_labels = []

        for category, texts in categories.items():
            for text in texts:
                all_texts.append(text)
                text_labels.append(category)

        embeddings = create_embeddings(all_texts, model)

        if embeddings:
            print(f"\n=== Text Classification Example ===")
            print(f"Total texts: {len(all_texts)}")
            print(f"Categories: {list(categories.keys())}")

            # Calculate similarities within categories
            for category in categories.keys():
                category_indices = [
                    i for i, label in enumerate(text_labels) if label == category
                ]
                category_embeddings = [embeddings[i] for i in category_indices]

                if len(category_embeddings) > 1:
                    avg_similarity = np.mean(
                        [
                            cosine_similarity([emb1], [emb2])[0][0]
                            for i, emb1 in enumerate(category_embeddings)
                            for j, emb2 in enumerate(category_embeddings)
                            if i != j
                        ]
                    )
                    print(
                        f"Average similarity within '{category}': {avg_similarity:.4f}"
                    )

        return embeddings, text_labels

    except Exception as e:
        print(f"Error in text classification: {e}")
        return None, None


def search_example(query, documents, model="text-embedding-ada-002"):
    """Example of semantic search using embeddings"""
    try:
        # Create embeddings for query and documents
        all_texts = [query] + documents
        response = client.embeddings.create(model=model, input=all_texts)

        query_embedding = response.data[0].embedding
        document_embeddings = [data.embedding for data in response.data[1:]]

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(document_embeddings):
            similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            similarities.append((similarity, documents[i]))

        # Sort by similarity
        similarities.sort(reverse=True)

        print(f"=== Semantic Search Example ===")
        print(f"Query: {query}")
        print(f"Number of documents: {len(documents)}")
        print("\nSearch Results (sorted by relevance):")
        for i, (similarity, document) in enumerate(similarities, 1):
            print(f"{i}. Similarity: {similarity:.4f} | Document: {document}")

        print(f"Usage: {response.usage}")

        return similarities

    except Exception as e:
        print(f"Error in search example: {e}")
        return None


if __name__ == "__main__":
    # Single text embedding
    single_text_embedding("Hello, world! This is a test of the embedding API.")

    print("\n" + "=" * 60 + "\n")

    # Multiple texts embedding
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast auburn fox leaps across a sleepy canine.",
        "The weather is sunny today.",
        "It's raining heavily outside.",
    ]
    embeddings = create_embeddings(texts)

    print("\n" + "=" * 60 + "\n")

    # Semantic similarity
    semantic_similarity(
        "The quick brown fox jumps over the lazy dog.",
        "A fast auburn fox leaps across a sleepy canine.",
    )

    print("\n" + "=" * 60 + "\n")

    # Text classification example
    text_classification_example()

    print("\n" + "=" * 60 + "\n")

    # Search example
    query = "What is machine learning?"
    documents = [
        "Machine learning is a subset of artificial intelligence.",
        "The weather forecast predicts rain tomorrow.",
        "Deep learning uses neural networks with multiple layers.",
        "Cooking requires patience and skill.",
        "AI systems can learn from data without explicit programming.",
    ]
    search_example(query, documents)
