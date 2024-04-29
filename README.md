## Voice Assistant integrated with chatgpt to be run on Raspberry Pi

## Features
- Wake word detection using Porcupine
- Speech recognition with Google Speech Recognition
- AI-based chat using ChatGPT 
- Text-to-Speech using Google Text-to-Speech (gTTS)
- Context-Aware interactions for chatGPT based on conversation history
- Increased Personalization functionality of LLM for User interaction
- Retrieval Augmented Generation

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/Voice-Based-AI-Assistant-with-ChatGPT-on-Raspberry-Pi.git
cd Voice-Based-AI-Assistant-with-ChatGPT-on-Raspberry-Pi
```
2. Update and install your Raspberry Pi packages:
```bash
sudo apt-get update
sudo apt-get upgrade
chmod +x install_dependencies.sh
./install_dependencies.sh
```
3. Set up a virtual environment and activate it
```bash
python3 -m venv env
#on Pi
source env/bin/activate
#on Windows
./env/bin/activate
```
4. Install the required packages
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```


## Usage
1. Run the main script:
```bash
python main.py
```
2. The assistant will listen for the wake word "Hey Ras Pi". Once detected, it will prompt you to speak your query.

3. The assistant will process your query using ChatGPT and provide an appropriate response.


