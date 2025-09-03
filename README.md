# LLM Bootcamp OpenAI Demo

A comprehensive collection of OpenAI API examples and use cases demonstrating various applications of AI technology, from basic API calls to advanced implementations with structured data and tool calling.

## 📁 Project Structure

### 🚀 **01_ALL_APIS** - Complete API Endpoints Collection
Comprehensive examples of all major OpenAI API endpoints:

- `01_models_listing.py` - List and explore available models
- `02_text_completions.py` - Basic text generation
- `03_chat_completions.py` - Multi-turn conversations
- `03.1_text_streaming.py` - Real-time streaming responses
- `04_embeddings.py` - Vector embeddings and similarity
- `05_image_generation.py` - AI-powered image creation
- `06_audio_transcription.py` - Speech-to-text transcription
- `07_content_moderation.py` - Safety and compliance checking
- `08_assistant_responses.py` - Tool-augmented AI agents
- `09_text_to_speech.py` - Text to Speech
- `img/` - Generated images from image generation examples
- `sample_audio_placeholder.txt` - Placeholder for audio transcription examples
- `README.md` - Detailed documentation for API examples

### 🎯 **02_USE_CASE** - Practical Use Cases
Real-world applications and implementations:

- `01_chatbot.py` - Basic chatbot implementation
- `02_chatbot_Streaming.py` - Streaming chatbot with real-time responses
- `03_SentimentAnalysis.py` - **Enhanced** sentiment analysis with Pydantic structured responses
- `04_SQLCoding.py` - **Advanced** SQL generation with tool calling and validation
- `05_Summary.py` - Text summarization
- `06_Translation.py` - Multi-language translation
- `example.db` - SQLite database for SQL examples

### 🤖 **03_AGENTS** - AI Agent Implementations
AI agent examples and implementations:

- `01_Agent.py` - Basic AI agent implementation
- `02_Agent_with_Tools.py` - AI agent with tool integration
- `README.md` - Documentation for agent examples

### 🏗️ **04_PROJECTS** - Advanced Projects
Advanced projects and applications (under development):

- `README.MD` - Project documentation (coming soon)

### 📚 **Root Level Files**
- `README.md` - Main project documentation
- `requirements.txt` - Project dependencies
- `.gitignore` - Git ignore rules

## 🚀 **Key Features**

### ✨ **Advanced Implementations**
- **Structured Responses** - Using Pydantic for type-safe data
- **Tool Calling** - Function calling for complex operations
- **Streaming** - Real-time response streaming
- **Error Handling** - Robust error management
- **Interactive Demos** - User-friendly CLI interfaces

### 🔧 **Technologies Used**
- **OpenAI API** - Latest GPT models and endpoints
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Database operations
- **Pandas** - Data manipulation
- **Python-dotenv** - Environment management

## 🛠️ **Setup**

### Prerequisites
- Python 3.8+
- OpenAI API key
- Required dependencies

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IDEAS-Incubator/LLM_Bootcamp_OpenAI
   cd LLM_Bootcamp_OpenAI
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   conda create -n openai_demo python=3.12
   conda activate openai_demo
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## 📖 **Usage**

### 🎮 **Interactive Demos**
Most scripts include interactive demos. Run any script to start:

```bash
# Sentiment Analysis with structured responses
cd 02_USE_CASE
python 03_SentimentAnalysis.py

# SQL Coding with tool calling
cd 02_USE_CASE
python 04_SQLCoding.py

# Streaming chatbot
cd 02_USE_CASE
python 02_chatbot_Streaming.py

# Basic chatbot
cd 02_USE_CASE
python 01_chatbot.py
```

### 🔧 **API Examples**
Run individual API examples:

```bash
# List available models
cd 01_ALL_APIS
python 01_models_listing.py

# Text completions
cd 01_ALL_APIS
python 02_text_completions.py

# Chat completions with streaming
cd 01_ALL_APIS
python 03.1_text_streaming.py

# Image generation
cd 01_ALL_APIS
python 05_image_generation.py

# Audio transcription
cd 01_ALL_APIS
python 06_audio_transcription.py

# Content moderation
cd 01_ALL_APIS
python 07_content_moderation.py

# Assistant responses with tools
cd 01_ALL_APIS
python 08_assistant_responses.py

# Real-time interaction
cd 01_ALL_APIS
python 09_realtime_interaction.py
```

### 🤖 **Agent Examples**
Run AI agent implementations:

```bash
# Basic agent
cd 03_AGENTS
python 01_Agent.py

# Agent with tools
cd 03_AGENTS
python 02_Agent_with_Tools.py
```

## 🎯 **Highlights**

### 🎨 **Enhanced Features**
- **Pydantic Integration** - Type-safe structured responses
- **Tool Calling** - Advanced function calling capabilities
- **Streaming Support** - Real-time response streaming
- **Interactive Interfaces** - User-friendly CLI demos
- **Error Recovery** - Robust error handling and validation

### 📊 **Use Cases Covered**
- **Sentiment Analysis** - Structured classification with confidence scores
- **SQL Generation** - Natural language to SQL with validation
- **Text Processing** - Summarization, translation, and analysis
- **Multimodal AI** - Text, images, audio, and real-time interactions
- **Agent Systems** - Tool-augmented AI agents
- **Content Moderation** - Safety and compliance checking
- **Embeddings** - Vector similarity and search

## 🔮 **Upcoming Projects**

The `04_PROJECTS` directory will contain advanced applications and real-world implementations:

- **Project 1** - TBD
- **Project 2** - TBD
- **Project 3** - TBD

## ⚠️ **Important Notes**

- Make sure you have set up your OpenAI API key before running the scripts
- Some features require specific OpenAI model access
- Monitor your API usage to manage costs
- Keep your API key secure and never commit it to version control
