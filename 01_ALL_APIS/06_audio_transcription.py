"""
LLM Bootcamp OpenAI Demo - Audio Transcription
POST /v1/audio/transcriptions - Transcribe audio to text
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import tempfile

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def transcribe_audio(audio_file_path, model="whisper-1"):
    """Transcribe audio file to text"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model, file=audio_file, response_format="text"
            )

        print(f"=== Audio Transcription ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Transcription: {response}")

        return response

    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def transcribe_audio_verbose(audio_file_path, model="whisper-1"):
    """Transcribe audio with verbose response format"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model, file=audio_file, response_format="verbose_json"
            )

        print(f"=== Verbose Audio Transcription ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Language: {response.language}")
        print(f"Duration: {response.duration}")
        print(f"Text: {response.text}")

        if hasattr(response, "segments"):
            print(f"Number of segments: {len(response.segments)}")
            for i, segment in enumerate(response.segments[:3]):  # Show first 3 segments
                print(
                    f"Segment {i+1}: {segment.text} (start: {segment.start}, end: {segment.end})"
                )

        return response

    except Exception as e:
        print(f"Error in verbose transcription: {e}")
        return None


def transcribe_audio_with_prompt(audio_file_path, prompt, model="whisper-1"):
    """Transcribe audio with a prompt to guide transcription"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model, file=audio_file, prompt=prompt, response_format="text"
            )

        print(f"=== Audio Transcription with Prompt ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Prompt: {prompt}")
        print(f"Transcription: {response}")

        return response

    except Exception as e:
        print(f"Error transcribing with prompt: {e}")
        return None


def transcribe_audio_timestamped(audio_file_path, model="whisper-1"):
    """Transcribe audio with timestamps"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="srt",  # SubRip format with timestamps
            )

        print(f"=== Timestamped Audio Transcription ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Transcription (SRT format):")
        print(response)

        return response

    except Exception as e:
        print(f"Error in timestamped transcription: {e}")
        return None


def download_sample_audio():
    """Download a sample audio file for testing"""
    try:
        # This is a placeholder - in a real scenario, you'd have your own audio files
        # For demonstration, we'll create a simple text file as a placeholder
        sample_text = """
        This is a sample audio transcription demo.
        The OpenAI Whisper model can transcribe audio files in various formats.
        It supports multiple languages and can provide timestamps.
        """

        with open("sample_audio_placeholder.txt", "w") as f:
            f.write(sample_text)

        print("Created sample audio placeholder file: sample_audio_placeholder.txt")
        print(
            "Note: In a real scenario, you would use actual audio files (.mp3, .wav, .m4a, etc.)"
        )

        return "sample_audio_placeholder.txt"

    except Exception as e:
        print(f"Error creating sample file: {e}")
        return None


def transcribe_examples():
    """Run various transcription examples"""
    print("=== Audio Transcription Examples ===")

    # Note: These examples assume you have audio files
    # In a real scenario, you would replace these with actual audio file paths

    # Example 1: Basic transcription
    print("\n1. Basic Transcription")
    print("To test this, replace 'sample_audio.mp3' with your actual audio file path")
    # transcribe_audio("sample_audio.mp3")

    # Example 2: Verbose transcription
    print("\n2. Verbose Transcription")
    print("To test this, replace 'sample_audio.mp3' with your actual audio file path")
    # transcribe_audio_verbose("sample_audio.mp3")

    # Example 3: Transcription with prompt
    print("\n3. Transcription with Prompt")
    print("To test this, replace 'sample_audio.mp3' with your actual audio file path")
    # transcribe_audio_with_prompt("sample_audio.mp3", "This audio contains technical terminology about machine learning.")

    # Example 4: Timestamped transcription
    print("\n4. Timestamped Transcription")
    print("To test this, replace 'sample_audio.mp3' with your actual audio file path")
    # transcribe_timestamped("sample_audio.mp3")


def supported_formats():
    """Show supported audio formats"""
    print("=== Supported Audio Formats ===")
    formats = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

    print("OpenAI Whisper supports the following audio formats:")
    for fmt in formats:
        print(f"- .{fmt}")

    print("\nFile size limit: 25 MB")
    print("Supported languages: 99+ languages")


def language_detection_example():
    """Example of language detection in transcription"""
    print("=== Language Detection Example ===")
    print("Whisper automatically detects the language of the audio.")
    print("You can also specify a language using the 'language' parameter:")
    print("- 'en' for English")
    print("- 'es' for Spanish")
    print("- 'fr' for French")
    print("- 'de' for German")
    print("- And many more...")


if __name__ == "__main__":
    # Show supported formats
    supported_formats()

    print("\n" + "=" * 60 + "\n")

    # Language detection info
    language_detection_example()

    print("\n" + "=" * 60 + "\n")

    # Create sample file for demonstration
    sample_file = download_sample_audio()

    print("\n" + "=" * 60 + "\n")

    # Show transcription examples
    transcribe_examples()

    print("\n" + "=" * 60 + "\n")
    print("Note: To test actual transcription, you need audio files.")
    print("Replace the commented lines with actual audio file paths.")
    print("Example usage:")
    print("transcribe_audio('path/to/your/audio.mp3')")
