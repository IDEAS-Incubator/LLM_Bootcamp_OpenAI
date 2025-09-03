# LLM Bootcamp OpenAI Demo

A comprehensive collection of OpenAI API use cases demonstrating all major endpoints and capabilities.

## Overview

This repository contains practical examples for all major OpenAI API endpoints, providing hands-on experience with:

- **Text Generation & Chat** - Basic completions and conversational AI
- **Embeddings** - Vector representations for semantic search and similarity
- **Image Generation** - AI-powered image creation and editing
- **Audio Processing** - Speech-to-text transcription
- **Content Moderation** - Safety and policy compliance
- **Assistant Responses** - Tool-augmented AI agents
- **Realtime Interactions** - Low-latency multimodal experiences

##  API Endpoints Covered

| Endpoint | Description | File |
|----------|-------------|------|
| `GET /v1/models` | List models and metadata | `01_models_listing.py` |
| `POST /v1/completions` | Text completion (single-prompt) | `02_text_completions.py` |
| `POST /v1/chat/completions` | Chat-style completion (multi-turn) | `03_chat_completions.py` |
| `POST /v1/embeddings` | Generate vector embeddings | `04_embeddings.py` |
| `POST /v1/images/generations` | Create or tweak images | `05_image_generation.py` |
| `POST /v1/audio/transcriptions` | Transcribe audio to text | `06_audio_transcription.py` |
| `POST /v1/moderations` | Check text against content policy | `07_content_moderation.py` |
| `POST /v1/responses` | Tool-augmented chat + agent functionality | `08_assistant_responses.py` |
| `POST /v1/realtime` | Low-latency multimodal interaction | `09_realtime_interaction.py` |

##  Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Required dependencies

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd LLM_Bootcamp_OpenAI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

##  Examples

### 1. Models Listing (`01_models_listing.py`)
```python
# List all available models
python 01_models_listing.py
```
- Lists all available OpenAI models
- Shows model metadata and capabilities
- Retrieves specific model details

### 2. Text Completions (`02_text_completions.py`)
```python
# Basic text completion
python 02_text_completions.py
```
- Basic text generation
- Creative writing with temperature control
- Code completion with specific parameters
- Structured output formatting

### 3. Chat Completions (`03_chat_completions.py`)
```python
# Multi-turn conversations
python 03_chat_completions.py
```
- Basic chat interactions
- Multi-turn conversations
- System prompts for behavior control
- Function calling examples
- Streaming responses

### 4. Embeddings (`04_embeddings.py`)
```python
# Vector embeddings and similarity
python 04_embeddings.py
```
- Text embedding generation
- Semantic similarity calculations
- Text classification examples
- Semantic search implementation

### 5. Image Generation (`05_image_generation.py`)
```python
# AI image generation
python 05_image_generation.py
```
- Text-to-image generation
- Image variations
- Image editing with masks
- Different styles and sizes

### 6. Audio Transcription (`06_audio_transcription.py`)
```python
# Speech-to-text conversion
python 06_audio_transcription.py
```
- Audio file transcription
- Multiple output formats
- Language detection
- Timestamped transcripts

### 7. Content Moderation (`07_content_moderation.py`)
```python
# Safety and policy compliance
python 07_content_moderation.py
```
- Text content moderation
- Multiple text processing
- Category-specific analysis
- Safety guidelines

### 8. Assistant Responses (`08_assistant_responses.py`)
```python
# Tool-augmented AI agents
python 08_assistant_responses.py
```
- Basic assistant responses
- Tool integration examples
- Multi-tool usage
- Conversation management

### 9. Realtime Interactions (`09_realtime_interaction.py`)
```python
# Low-latency interactions
python 09_realtime_interaction.py
```
- Fast response times
- Interactive applications
- Latency comparisons
- Multimodal interactions

##  Key Features

### Text Processing
- **Completions**: Single-prompt text generation
- **Chat**: Multi-turn conversational AI
- **Embeddings**: Vector representations for semantic analysis

### Multimodal Capabilities
- **Image Generation**: Create images from text descriptions
- **Audio Transcription**: Convert speech to text
- **Content Moderation**: Ensure safety and compliance

### Advanced Features
- **Function Calling**: Tool integration for enhanced capabilities
- **Streaming**: Real-time response generation
- **System Prompts**: Behavior customization
- **Realtime API**: Low-latency interactions

##  Use Cases

### Business Applications
- **Customer Support**: AI-powered chatbots
- **Content Creation**: Automated text and image generation
- **Data Analysis**: Semantic search and classification
- **Safety**: Content moderation and compliance

### Development
- **Code Generation**: AI-assisted programming
- **Documentation**: Automated content creation
- **Testing**: AI-powered test generation
- **Debugging**: Intelligent error analysis

### Research & Education
- **Language Learning**: Multilingual support
- **Research Analysis**: Semantic similarity and clustering
- **Educational Content**: Automated lesson generation
- **Accessibility**: Audio transcription and translation

##  Best Practices

### API Usage
- **Rate Limiting**: Respect API rate limits
- **Error Handling**: Implement robust error handling
- **Cost Management**: Monitor usage and costs
- **Security**: Secure API key storage

### Content Safety
- **Moderation**: Always moderate user-generated content
- **Guidelines**: Follow OpenAI's content policy
- **Monitoring**: Regular content review
- **User Feedback**: Collect and act on user reports

### Performance
- **Caching**: Cache frequently used embeddings
- **Batching**: Process multiple requests efficiently
- **Streaming**: Use streaming for real-time applications
- **Optimization**: Choose appropriate models and parameters

##  Examples by Category

### Basic Text Generation
```python
# Simple completion
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Explain quantum computing",
    max_tokens=100
)
```

### Conversational AI
```python
# Multi-turn chat
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"}
    ]
)
```

### Semantic Analysis
```python
# Text embeddings
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Your text here"
)
```

### Image Generation
```python
# Generate image
response = client.images.generate(
    model="dall-e-3",
    prompt="A beautiful sunset over mountains",
    size="1024x1024"
)
```

### Audio Processing
```python
# Transcribe audio
with open("audio.mp3", "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
```

### Content Moderation
```python
# Moderate content
response = client.moderations.create(
    input="Text to moderate"
)
```

##  Important Notes

### API Keys
- Keep your API key secure and never commit it to version control
- Use environment variables for API key storage
- Rotate keys regularly for security

### Rate Limits
- Monitor your API usage to stay within limits
- Implement retry logic with exponential backoff
- Consider using different models for different use cases

### Costs
- Different models have different pricing
- Monitor usage through OpenAI dashboard
- Implement cost controls in production

### Model Availability
- Some models may be region-restricted
- Check model availability before deployment
- Consider fallback options

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Add your examples or improvements
4. Test thoroughly
5. Submit a pull request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Community](https://community.openai.com/)
- [API Reference](https://platform.openai.com/docs/api-reference)

##  Support

For questions or issues:
- Check the OpenAI documentation
- Review the examples in this repository
- Consult the OpenAI community forums
- Contact OpenAI support for API-specific issues

---

