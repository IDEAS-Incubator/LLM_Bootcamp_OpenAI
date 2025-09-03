# LLM Bootcamp OpenAI Demo


This repository contains a collection of Python scripts demonstrating various applications of OpenAI's API, including basic API calls, chatbots, sentiment analysis, SQL coding assistance, translation, and summarization.

## Project Structure

- `01_Basic_API_Call.py` - Basic example of making API calls to OpenAI
- `02_chatbot.py` - Implementation of a simple chatbot using OpenAI's API
- `03_SentimentAnalysis.py` - Sentiment analysis of text using OpenAI
- `04_SQLCoding.py` - SQL query generation and assistance using OpenAI
- `05_Summary.py` - Text summarization using OpenAI
- `06_Translation.py` - Text translation using OpenAI
- `07_Agent.py` - An Agent demo
- `07_Agent_With_Tools.py` - An Agent demo
- `example.db` - SQLite database used for SQL coding examples
- `requirements.txt` - Project dependencies

## Setup

1. Clone the repository:
```bash
git clone https://github.com/IDEAS-Incubator/LLM_Bootcamp_OpenAI

```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`


## Usage

Each script in this repository demonstrates a different use case of the OpenAI API. To run any script:

```bash
python script_name.py
```

## Tips
Make sure you have set up your OpenAI API key before running the scripts.
