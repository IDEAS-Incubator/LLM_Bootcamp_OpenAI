from pathlib import Path
from openai import OpenAI
import os
import argparse
from dotenv import load_dotenv


def create_speech_folder():
    """Create speech folder if it doesn't exist"""
    speech_folder = Path(__file__).parent / "speech"
    speech_folder.mkdir(exist_ok=True)
    return speech_folder


def generate_speech(
    text, voice="coral", model="gpt-4o-mini-tts", instructions="", filename=None
):
    """Generate speech from text and save to file"""
    load_dotenv()
    client = OpenAI()

    # Create speech folder
    speech_folder = create_speech_folder()

    # Generate filename if not provided
    if filename is None:
        # Create a safe filename from the first few words of the text
        safe_text = "".join(
            c for c in text[:30] if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_text = safe_text.replace(" ", "_")
        filename = f"{safe_text}.mp3"

    # Ensure filename has .mp3 extension
    if not filename.endswith(".mp3"):
        filename += ".mp3"

    speech_file_path = speech_folder / filename

    print(f"Generating speech for: '{text}'")
    print(f"Voice: {voice}")
    print(f"Model: {model}")
    if instructions:
        print(f"Instructions: {instructions}")
    print(f"Saving to: {speech_file_path}")

    try:
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            instructions=instructions,
        ) as response:
            response.stream_to_file(speech_file_path)

        print(f"✅ Speech saved successfully to: {speech_file_path}")
        return str(speech_file_path)

    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate speech from text using OpenAI TTS"
    )
    parser.add_argument(
        "--text",
        "-t",
        default="Today is a wonderful day to build something people love!",
        help="Text to convert to speech",
    )
    parser.add_argument(
        "--voice",
        "-v",
        default="coral",
        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        help="Voice to use for speech generation",
    )
    parser.add_argument(
        "--model", "-m", default="gpt-4o-mini-tts", help="TTS model to use"
    )
    parser.add_argument(
        "--instructions",
        "-i",
        default="",
        help="Additional instructions for speech generation",
    )
    parser.add_argument(
        "--filename",
        "-f",
        default=None,
        help="Output filename (without .mp3 extension)",
    )

    args = parser.parse_args()

    # Generate speech
    result = generate_speech(
        text=args.text,
        voice=args.voice,
        model=args.model,
        instructions=args.instructions,
        filename=args.filename,
    )

    if result:
        print(f"\n🎉 Speech generation completed!")
        print(f"📁 File location: {result}")
    else:
        print("\n❌ Speech generation failed!")


if __name__ == "__main__":
    main()
