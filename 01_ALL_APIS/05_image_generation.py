"""
LLM Bootcamp OpenAI Demo - Image Generation
POST /v1/images/generations - Create or tweak images
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from PIL import Image
import io

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_image(prompt, size="1024x1024", quality="standard", style="vivid"):
    """Generate an image from a text prompt"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1,
        )

        print(f"=== Image Generation ===")
        print(f"Prompt: {prompt}")
        print(f"Size: {size}")
        print(f"Quality: {quality}")
        print(f"Style: {style}")
        print(f"Image URL: {response.data[0].url}")
        print(f"Usage: {response.usage}")

        return response.data[0].url

    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def generate_image_variations(image_path, size="1024x1024"):
    """Generate variations of an existing image"""
    try:
        with open(image_path, "rb") as image_file:
            response = client.images.create_variation(image=image_file, size=size, n=1)

        print(f"=== Image Variations ===")
        print(f"Original image: {image_path}")
        print(f"Size: {size}")
        print(f"Variation URL: {response.data[0].url}")

        return response.data[0].url

    except Exception as e:
        print(f"Error creating image variation: {e}")
        return None


def edit_image(image_path, mask_path, prompt, size="1024x1024"):
    """Edit an image using a mask and prompt"""
    try:
        with open(image_path, "rb") as image_file:
            with open(mask_path, "rb") as mask_file:
                response = client.images.edit(
                    image=image_file, mask=mask_file, prompt=prompt, size=size, n=1
                )

        print(f"=== Image Editing ===")
        print(f"Original image: {image_path}")
        print(f"Mask: {mask_path}")
        print(f"Prompt: {prompt}")
        print(f"Size: {size}")
        print(f"Edited image URL: {response.data[0].url}")

        return response.data[0].url

    except Exception as e:
        print(f"Error editing image: {e}")
        return None


def download_image(url, filename):
    """Download an image from URL and save it locally"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Save the image
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Image downloaded and saved as: {filename}")

        # Display image info
        image = Image.open(filename)
        print(f"Image size: {image.size}")
        print(f"Image mode: {image.mode}")

        return filename

    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def creative_image_examples():
    """Generate various creative image examples"""
    examples = [
        {
            "prompt": "A futuristic cityscape with flying cars and neon lights, digital art style",
            "filename": "futuristic_city.png",
        },
        {
            "prompt": "A serene mountain landscape at sunset with a crystal clear lake reflecting the sky",
            "filename": "mountain_sunset.png",
        },
        {
            "prompt": "A cute robot playing with a cat in a cozy living room, warm lighting",
            "filename": "robot_cat.png",
        },
        {
            "prompt": "An underwater scene with colorful coral reefs and tropical fish",
            "filename": "underwater_scene.png",
        },
    ]

    print("=== Creative Image Examples ===")

    for example in examples:
        print(f"\nGenerating: {example['prompt']}")
        url = generate_image(example["prompt"])

        if url:
            # Download the image
            download_image(url, example["filename"])

        print("-" * 50)


def different_styles_example():
    """Generate the same prompt with different styles"""
    prompt = "A beautiful garden with flowers and butterflies"

    styles = ["vivid", "natural"]

    print("=== Different Styles Example ===")
    print(f"Base prompt: {prompt}")

    for style in styles:
        print(f"\nGenerating with style: {style}")
        url = generate_image(prompt, style=style)

        if url:
            filename = f"garden_{style}.png"
            download_image(url, filename)

        print("-" * 50)


def different_sizes_example():
    """Generate the same prompt with different sizes"""
    prompt = "A minimalist coffee cup on a wooden table"

    sizes = ["1024x1024", "1792x1024", "1024x1792"]

    print("=== Different Sizes Example ===")
    print(f"Base prompt: {prompt}")

    for size in sizes:
        print(f"\nGenerating with size: {size}")
        url = generate_image(prompt, size=size)

        if url:
            filename = f"coffee_cup_{size.replace('x', '_')}.png"
            download_image(url, filename)

        print("-" * 50)


if __name__ == "__main__":
    # Basic image generation
    generate_image("A majestic dragon flying over a medieval castle at sunset")

    print("\n" + "=" * 60 + "\n")

    # Creative examples
    creative_image_examples()

    print("\n" + "=" * 60 + "\n")

    # Different styles
    different_styles_example()

    print("\n" + "=" * 60 + "\n")

    # Different sizes
    different_sizes_example()

    # Note: Image variations and editing require actual image files
    # Uncomment the following lines if you have image files to test with

    # # Image variations (requires an image file)
    # # generate_image_variations("path/to/your/image.png")

    # # Image editing (requires image and mask files)
    # # edit_image("path/to/image.png", "path/to/mask.png", "Add a rainbow to the sky")
