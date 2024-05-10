# Streamlit Webapp

## Installation

Note: You need Python 3.10 or above.

1. Create a virtual environment (venv):
    ```sh
    python -m venv path-to-venv
    ```
   `venv` stands for Virtual Environment.

2. Activate the virtual environment:
    ```sh
    source path-to-venv/bin/activate
    ```
    On Windows:
    ```sh
    .\venv\Scripts\activate
    ```

3. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```

## Running

### OpenAI Bot

#### OpenAI Chatbot
* **Models:** gpt-3.5-turbo, gpt-4-turbo-preview, gpt-4-vision-preview

1. Go to `bot/openai-bot`
2. Run:
    ```sh
    streamlit run bot-openai-chat.py
    ```

#### OpenAI Image Bot
* **Models:** dall-e-3, dall-e-2

1. Go to `bot/openai-bot`
2. Run:
    ```sh
    streamlit run bot-openai-image.py
    ```

### Langchain Agent Bot

A Langchain agent uses an LLM to make a decision to use which tools. The current app has to 4 tools and uses GPT3.5-Turbo for decision making as well as answering some questions that can answer directly. The model is not good at following the descriptions. It is supposed to pass through the answers, but it changes some words in the final answer.

#### List of Tools
1. GPT4-Turbo_General_Assistant
2. GPT4-Turbo_Code_Assistant
3. GPT35-Turbo_Code_Assistant
4. Dalle3_Image_Generator

1. Go to `bot/langchain-bot`
2. Run:
    ```sh
    streamlit run bot-langchain-chat.py
    ```

### Indexing

1. Go to `bot/rag_indexing`
2. Run:
    ```sh
    python indexing.py [url]
    ```
   For example:
   ```sh
   python indexing.py https://lilianweng.github.io/posts/2023-06-23-agent/

