from datetime import datetime as dt
import json
import os
import requests

from playsound import playsound

import guide_config
from holon import logger
from holon.HolonicAgent import HolonicAgent

class PlayHTVoice(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)


    def __tts(self, text):
        url = "https://play.ht/api/v2/tts"
        headers = {
            "AUTHORIZATION": f"Bearer {guide_config.playht_secret_key}",
            "X-USER-ID": f"{guide_config.playht_user_id}",
            "accept": "text/event-stream",
            "content-type": "application/json",
        }
        data = {
            "text": text,
            "voice": "larry"
        }

        voice_url = None
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            event = None
            data = None

            for line in response.iter_lines(decode_unicode=True):
                line = line.strip()
                if not line:
                    continue
                
                key, value = tuple([pair.strip() for pair in line.split(":", 1)])
                if key == "event":
                    event = value
                elif key == "data":
                    try:
                        data = json.loads(value)
                    except Exception as ex:
                        logger.error(ex)

                if event and data:
                    if event == "completed":
                        voice_url = data["url"]
                    event = None
                    data = None
        else:
            print(f"Request failed with status code: {response.status_code}")

        return voice_url


    def __speak(self, voice_url):
        response = requests.get(voice_url)
        temp_filename = dt.now().strftime(f"speak-%m%d-%H%M-%S.mp3")
        temp_filepath = os.path.join(guide_config.output_dir, temp_filename)
        # temp_filename = "_test/temp.mp3"
        with open(temp_filepath, "wb") as f:
            f.write(response.content)
        playsound(temp_filepath)
        os.remove(temp_filepath)
        self.publish("voice.spoken")


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("voice.text")

        super()._on_connect(client, userdata, flags, rc)


    def _on_topic(self, topic, data):
        if "voice.text" == topic:
            try:
                voice_url = self.__tts(text=data)
                self.__speak(voice_url)
            except Exception as ex:
                logger.error(ex)

        super()._on_topic(topic, data)
