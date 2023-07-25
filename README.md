# Hola Dialog


## Introduction
This program uses the hierarchical structure of [Agent BDI](https://github.com/mfshiu/agent-bdi) to display the features of voice input, semantic understanding, action execution and voice output. Voice input is translated into text using [OpenAI Whisper](https://github.com/openai/whisper); semantic understanding is performed through ChatGPT; voice output uses [conqui ai](https://github.com/coqui-ai/TTS) as test-to-speech. Action execution is mainly based on simulation, and ROS will be integrated in the future.


## Installation
1. Install the required packages.
````
sudo apt-get install portaudio19-dev
````
2. Install the required packages.
````
pip install -r requirements.txt
````
3. Create guide_config.py, rewite settings such as mqtt and openai key. 
````
cp guide_config.sample.py guide_config.py
````
4. Start the main program in one Nvidia supported machine.
````
python start.py
````
5. Start the transcription program in another Nvidia supported machine.
````
python run_trans.py
````