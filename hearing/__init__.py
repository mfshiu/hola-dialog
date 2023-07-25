import os, sys

from helper import logger
from holon import logger
from holon.HolonicAgent import HolonicAgent
from hearing.microphone import Microphone

class Hearing(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.head_agents.append(Microphone(cfg))


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("microphone.wave_path")

        super()._on_connect(client, userdata, flags, rc)


    def _on_topic(self, topic, data):
        if "microphone.wave_path" == topic:
            filepath = data
            logger.debug(f"wave_path:{filepath}")
            try:
                with open(filepath, "rb") as file:
                    file_content = file.read()
                logger.debug(f'publish: hearing.voice')
                self.publish("hearing.voice", file_content)
                os.remove(filepath)
            except Exception as ex:
                logger.exception(ex)

        super()._on_topic(topic, data)
