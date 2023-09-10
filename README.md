# Hola Dialog
This program uses the framework of [Agent BDI](https://github.com/mfshiu/agent-bdi) to demonstrate the features of robot dialogue, including voice input, semantic understanding, action execution and voice output. Voice input is translated into text using [OpenAI Whisper](https://github.com/openai/whisper); semantic understanding is performed through ChatGPT; voice output uses [conqui ai](https://github.com/coqui-ai/TTS) as test-to-speech. Action execution is mainly based on simulation, and ROS will be integrated in the future.

The robot already have the ability to respond to greetings and simulate leading the way.


## Setup
Initialize and activate the virtual environment, making sure to use the validated Python version 3.10.11. Subsequently, install the required packages. The operating system compatibility includes Ubuntu 20.04 and Ubuntu 22.04.
````
sudo apt-get install portaudio19-dev
pip install -r requirements.txt
````
Create guide_config.py, rewite settings such as mqtt and openai key. 
````
cp guide_config.sample.py guide_config.py
````
Start the main program in one Nvidia supported machine.
````
python start.py
````
Start the transcription program in another Nvidia supported machine.
````
python run_trans.py
````
