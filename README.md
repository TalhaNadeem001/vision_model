## Voice Assistant integrated with chatgpt to be run on Raspberry Pi

## Features
- Wake word detection using Porcupine
- Speech recognition with Google Speech Recognition
- AI-based chat using ChatGPT 
- Text-to-Speech using Google Text-to-Speech (gTTS)
- Context-Aware interactions for chatGPT based on conversation history
- Increased Personalization functionality of LLM for User interaction
- Can act as a teacher for any document you upload

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

## Configuration
Before running the project, you need to create a `config.py` file in the `src` directory with your API keys. Use the provided `config_example.py` as a template and fill in the necessary information.
### Openai API
Refer to https://platform.openai.com/examples
### PicoVoice Access Key
Get your PicoVoice access key from the [PicoVoice Console](https://picovoice.ai/ "PicoVoice Console"). Add the access key to the `config.py` file.
### Bing API
This project uses an unofficial BING API from [EdgeGPT](https://github.com/acheong08/EdgeGPT "EdgeGPT"). To generate a cookies.json file for use with the BING API, follow the instructions in the EdgeGPT repository.<br />
Once you have your config.py and cookies.json files ready, you can proceed with running the project.
### Audio setup
Refer to https://www.youtube.com/watch?v=vEMzN5RgXbw&ab_channel=AssemblyAI

## Usage
1. Run the main script:
```bash
python main.py
```
2. The assistant will listen for the wake word "Hey Ras Pi". Once detected, it will prompt you to speak your query.

3. The assistant will process your query using ChatGPT and Bing APIs and provide an appropriate response.

## Directory Structure
```bash
.
├── ./.gitignore
├── ./README.md
├── ./cookies.json
├── ./env
├── ./install_dependencies.sh
├── ./main.py
├── ./models
│   ├── ./models/Hey-Ras-Pi_en_raspberry-pi_v2_1_0.ppn
│   ├── ./models/Hey-Ras-Pi_en_raspberry-pi_v2_1_0.zip
│   └── ./models/alexa_windows.ppn
├── ./output.mp3
├── ./requirements.txt
└── ./src
    ├── ./src/bing.py
    ├── ./src/config.py
    ├── ./src/config_example.py
    ├── ./src/gpt.py
    ├── ./src/nlp.py
    ├── ./src/speech_to_text.py
    ├── ./src/text_to_speech.py
    ├── ./src/translator.py
    └── ./src/wake_up_detect.py
└── ./wake_up_sound.wav
```
## Sample Output
![image](https://user-images.githubusercontent.com/49149560/230957752-df775470-8911-4e88-b1d0-a5e4e23e4347.png)
