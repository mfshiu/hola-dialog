from datetime import datetime as dt
import os

from playsound import playsound

import app_config
import helper
from holon.HolonicAgent import HolonicAgent


logger = helper.get_logger()


class Speaker(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)


    def _on_connect(self):
        self._subscribe("voice.wave")

        super()._on_connect()


    def _on_message(self, topic:str, payload):
        if "voice.wave" == topic:
            try:
                filename = dt.now().strftime(f"wave-%m%d-%H%M-%S.wav")
                filepath = os.path.join(app_config.output_dir, filename)
                with open(filepath, "wb") as file:
                    file.write(payload)
                logger.debug(f'playsound: {filepath}')
                playsound(filepath)
                os.remove(filepath)
            except Exception as ex:
                logger.exception(ex)
