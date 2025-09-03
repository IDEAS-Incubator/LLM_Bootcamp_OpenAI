# Speech Folder

This folder contains generated speech files from the OpenAI Text-to-Speech API.

## Usage

### CLI Options

The `09_text_to_speech.py` script now supports command-line arguments:

```bash
python 09_text_to_speech.py [OPTIONS]
```

### Available Options

- `--text, -t`: Text to convert to speech (default: "Today is a wonderful day to build something people love!")
- `--voice, -v`: Voice to use (choices: alloy, echo, fable, onyx, nova, shimmer, default: coral)
- `--model, -m`: TTS model to use (default: gpt-4o-mini-tts)
- `--instructions, -i`: Additional instructions for speech generation
- `--filename, -f`: Output filename (without .mp3 extension)

### Examples

1. **Default usage:**
   ```bash
   python 09_text_to_speech.py
   ```

2. **Custom text:**
   ```bash
   python 09_text_to_speech.py --text "Hello world!" --filename hello
   ```

3. **Different voice:**
   ```bash
   python 09_text_to_speech.py --text "This is Nova speaking" --voice nova
   ```

4. **With instructions:**
   ```bash
   python 09_text_to_speech.py --text "Welcome!" --instructions "Speak in a cheerful tone"
   ```

5. **Show help:**
   ```bash
   python 09_text_to_speech.py --help
   ```

### Voice Options

- **alloy**: Neutral, balanced voice
- **echo**: Warm, friendly voice
- **fable**: Storytelling voice
- **onyx**: Deep, authoritative voice
- **nova**: Bright, energetic voice
- **shimmer**: Soft, gentle voice
- **coral**: Default voice (cheerful and positive)

### File Organization

All generated speech files are automatically saved to this `speech/` folder with:
- Automatic filename generation based on text content
- .mp3 extension
- Safe filename characters only



