"""
LLM Bootcamp OpenAI Demo - Audio Transcription
POST /v1/audio/transcriptions - Transcribe audio to text
"""

from openai import OpenAI
import os
import argparse
from dotenv import load_dotenv
import requests
import tempfile
from pathlib import Path

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def create_transcriptions_folder():
    """Create transcriptions folder if it doesn't exist"""
    transcriptions_folder = Path(__file__).parent / "transcriptions"
    transcriptions_folder.mkdir(exist_ok=True)
    return transcriptions_folder


def transcribe_audio(
    audio_file_path, model="whisper-1", output_format="text", output_file=None
):
    """Transcribe audio file to text"""
    try:
        # Validate file exists
        if not os.path.exists(audio_file_path):
            print(f"❌ Error: Audio file '{audio_file_path}' not found")
            return None

        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model, file=audio_file, response_format=output_format
            )

        print(f"=== Audio Transcription ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Output format: {output_format}")

        if output_format == "text":
            print(f"Transcription: {response}")
        elif output_format == "verbose_json":
            print(f"Language: {response.language}")
            print(f"Duration: {response.duration}")
            print(f"Text: {response.text}")
        else:
            print(f"Transcription: {response}")

        # Save to file if requested
        if output_file:
            transcriptions_folder = create_transcriptions_folder()
            output_path = transcriptions_folder / output_file

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(str(response))

            print(f"✅ Transcription saved to: {output_path}")

        return response

    except Exception as e:
        print(f"❌ Error transcribing audio: {e}")
        return None


def transcribe_audio_verbose(audio_file_path, model="whisper-1", output_file=None):
    """Transcribe audio with verbose response format"""
    return transcribe_audio(audio_file_path, model, "verbose_json", output_file)


def transcribe_audio_with_prompt(
    audio_file_path, prompt, model="whisper-1", output_file=None
):
    """Transcribe audio with a prompt to guide transcription"""
    try:
        # Validate file exists
        if not os.path.exists(audio_file_path):
            print(f"❌ Error: Audio file '{audio_file_path}' not found")
            return None

        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model, file=audio_file, prompt=prompt, response_format="text"
            )

        print(f"=== Audio Transcription with Prompt ===")
        print(f"Audio file: {audio_file_path}")
        print(f"Model: {model}")
        print(f"Prompt: {prompt}")
        print(f"Transcription: {response}")

        # Save to file if requested
        if output_file:
            transcriptions_folder = create_transcriptions_folder()
            output_path = transcriptions_folder / output_file

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(str(response))

            print(f"✅ Transcription saved to: {output_path}")

        return response

    except Exception as e:
        print(f"❌ Error transcribing with prompt: {e}")
        return None


def transcribe_audio_timestamped(audio_file_path, model="whisper-1", output_file=None):
    """Transcribe audio with timestamps"""
    return transcribe_audio(audio_file_path, model, "srt", output_file)


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


def list_audio_files():
    """List available audio files in the transcriptions folder"""
    transcriptions_folder = create_transcriptions_folder()
    audio_extensions = [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"]

    print("=== Available Audio Files in Transcriptions Folder ===")

    audio_files = []
    for file_path in transcriptions_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
            audio_files.append(file_path)

    if audio_files:
        print(f"Found {len(audio_files)} audio file(s):")
        for i, file_path in enumerate(audio_files, 1):
            file_size = file_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            print(f"{i}. {file_path.name} ({size_mb:.2f} MB)")

        print("\n💡 Usage examples:")
        print(
            f"   python 06_audio_transcription.py transcriptions/{audio_files[0].name}"
        )
        print(
            f"   python 06_audio_transcription.py transcriptions/{audio_files[0].name} --format srt"
        )
        print(
            f"   python 06_audio_transcription.py transcriptions/{audio_files[0].name} --output custom_name"
        )
    else:
        print("No audio files found in the transcriptions folder.")
        print("Supported formats: .mp3, .mp4, .mpeg, .mpga, .m4a, .wav, .webm")
        print("Please add audio files to the transcriptions folder and try again.")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI Whisper"
    )
    parser.add_argument("audio_file", help="Path to the audio file to transcribe")
    parser.add_argument(
        "--model", "-m", default="whisper-1", help="Whisper model to use"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "verbose_json", "srt", "vtt"],
        default="text",
        help="Output format for transcription",
    )
    parser.add_argument("--output", "-o", help="Output file name (without extension)")
    parser.add_argument("--prompt", "-p", help="Prompt to guide transcription")
    parser.add_argument(
        "--show-formats", action="store_true", help="Show supported audio formats"
    )
    parser.add_argument(
        "--show-languages", action="store_true", help="Show language detection info"
    )
    parser.add_argument(
        "--list-audio",
        action="store_true",
        help="List available audio files in transcriptions folder",
    )

    args = parser.parse_args()

    # Show information if requested
    if args.show_formats:
        supported_formats()
        return

    if args.show_languages:
        language_detection_example()
        return

    if args.list_audio:
        list_audio_files()
        return

    # Handle file path - if it's just a filename, assume it's in transcriptions folder
    audio_file_path = args.audio_file
    if not os.path.exists(audio_file_path):
        # Try to find it in transcriptions folder
        transcriptions_folder = create_transcriptions_folder()
        possible_path = transcriptions_folder / audio_file_path
        if possible_path.exists():
            audio_file_path = str(possible_path)
            print(f"📁 Found audio file in transcriptions folder: {audio_file_path}")
        else:
            print(f"❌ Error: Audio file '{args.audio_file}' not found")
            print(f"💡 Try using --list-audio to see available files")
            return

    # Generate output filename if not provided
    if args.output is None:
        audio_name = Path(audio_file_path).stem
        if args.format == "text":
            args.output = f"{audio_name}_transcription.txt"
        elif args.format == "verbose_json":
            args.output = f"{audio_name}_transcription_verbose.json"
        elif args.format == "srt":
            args.output = f"{audio_name}_transcription.srt"
        elif args.format == "vtt":
            args.output = f"{audio_name}_transcription.vtt"

    # Perform transcription
    print(f"🎤 Transcribing: {audio_file_path}")
    print(f"📝 Model: {args.model}")
    print(f"📄 Format: {args.format}")

    if args.prompt:
        print(f"💡 Prompt: {args.prompt}")
        result = transcribe_audio_with_prompt(
            args.audio_file, args.prompt, args.model, args.output
        )
    else:
        result = transcribe_audio(args.audio_file, args.model, args.format, args.output)

    if result:
        print(f"\n🎉 Transcription completed successfully!")
        if args.output:
            transcriptions_folder = create_transcriptions_folder()
            output_path = transcriptions_folder / args.output
            print(f"📁 Saved to: {output_path}")
    else:
        print("\n❌ Transcription failed!")


if __name__ == "__main__":
    # If no arguments provided, show demo
    import sys

    if len(sys.argv) == 1:
        print("🎤 Audio Transcription Demo")
        print("=" * 50)

        supported_formats()
        print("\n" + "=" * 60 + "\n")

        language_detection_example()
        print("\n" + "=" * 60 + "\n")

        print("📖 Usage Examples:")
        print("1. Basic transcription:")
        print("   python 06_audio_transcription.py audio_file.mp3")
        print("\n2. With custom output file:")
        print(
            "   python 06_audio_transcription.py audio_file.mp3 --output my_transcript"
        )
        print("\n3. With prompt:")
        print(
            "   python 06_audio_transcription.py audio_file.mp3 --prompt 'This contains technical terms'"
        )
        print("\n4. Timestamped output:")
        print("   python 06_audio_transcription.py audio_file.mp3 --format srt")
        print("\n5. Show supported formats:")
        print("   python 06_audio_transcription.py --show-formats")
        print("\n6. Show help:")
        print("   python 06_audio_transcription.py --help")

        print("\n" + "=" * 60 + "\n")
        print("💡 Note: Replace 'audio_file.mp3' with your actual audio file path")
    else:
        main()
