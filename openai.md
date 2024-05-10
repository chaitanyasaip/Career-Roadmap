# OpenAI APIs
OpenAI API is a simple restful api. But the have **Python** and **Node.js** packages built on top of the api. We are using the Python package.

## Installation and Setup
* **Python:** 
    * **Windows & MacOS:** Go to [Python3.11](https://www.python.org/downloads/release/python-3118/) and find the link in the page and follow the installer.
    * **WSL2 & Ubuntu:** 
        1. run ```sudo apt update && sudo apt upgrade```.
        2. Check the Python version: ```python -V```.
        3. If you need to update the python, run 
        ```sudo apt upgrade python3```.
* **Virtual Environment:** 
    1. Create a venv: 
    ```python -m venv path-to-venv```  
    venv stands for Virtual Environment.
    2. Activate the venv:  
    **Linux & MacOS:** ```source path-to-venv/bin/activate```.
    **Windows:** ```path-to-venv\Scripts\activate```.
* **VS Code:** 
    1. Install Python Extension:  
    ```Extensions > search Python > Install microsoft.com Python extension```.  
    2. Choose the Python interpreter from your venv:  
    ```Settings > Command Palette > Python: Select interpreter > Enter interpreter path > Find > Path-to-env/bin/activate```.
    3. Choose the kernel for notebooks.
* **Set up API Key:** We use ```dotenv``` package and ```.env``` file. This way can work for all similar APIs.
    1. In each venv install ```dotenv``` package by ```pip install dotenv```. 
    2. In each project folder create ```.env``` file. In this file add the following line: ```OPENAI_API_KEY=key```.
    3. At the top of the main file of your project, add the following two lines:  
    ```from dotenv import load_dotenv```  
    ```load_dotenv()```

## Models
* **API Structure:** The API interface is very simple. You just need a client to call any of the models. The following two lines import the needed class and create an instance of it:
```
from openai import OpenAI
client = OpenAI()
```
* **Models List**
    * **GPT-4 Turbo** accessed by handle ```gpt-4-turbo-preview``` or any of the following handles.
        1. ```gpt-4-0125-preview``` Context Window: 128 k, Training Data: Up to Dec 2023.
        2. ```gpt-4-1106-preview``` Context Window: 128 k, Training Data: Up to Apr 2023.
        3. ```gpt-4-1106-vision-preview``` Context Window: 128 k, Training Data: Up to Apr 2023. Understands images.
    * **GPT-3.5 Turbo** accessed by handle ```gpt-3.5-turbo```
        1. ```gpt-3.5-turbo-0125``` Context Window: 32 k, Training Data: Up to Sep 2021.
    * **DALL-E**
        1. ```dall-e-3``` released Nov 2023
        2. ```dall-e-2``` released Nov 2022
    * **TTS** Text to natural sounding spoken text.
        1. ```tts-1```
        2. ```tts-1-hd```
    * **Whisper** general-purpose speech recognition model.
    * **Embeddings** numerical representation of text for semantic similarity and semantic search.
        1. ```text-embeddings-3-large``` Output dimension: 3072
        2. ```text-embeddings-3-small``` Output dimension: 1536
        3. ```text-embeddings-ada-002``` Output dimension: 1536 (oldest)

