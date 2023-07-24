import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from datetime import datetime as dt
import queue
import time

import whisper
import torch

import guide_config
from holon.HolonicAgent import HolonicAgent
import Helper
from Helper import logger


class Transcriptionist(HolonicAgent):
    def __init__(self, cfg):
        Helper.ensure_directory(guide_config.input_dir)
        super().__init__(cfg)


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("hearing.voice")

        super()._on_connect(client, userdata, flags, rc)


    def _on_message(self, client, db, msg):
        if "hearing.voice" == msg.topic:
            filename = dt.now().strftime(f"voice-%m%d-%H%M-%S.wav")
            wave_path = os.path.join(guide_config.input_dir, filename)
            # wave_path = dt.now().strftime("tests/_input/voice-%m%d-%H%M-%S.wav")
            with open(wave_path, "wb") as file:
                file.write(msg.payload)
            self.wave_queue.put(wave_path)


    def _run_begin(self):
        super()._run_begin()

        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.warning(f'Device of Whisper:{device}')
        self.wave_queue = queue.Queue()

        # whisper.DecodingOptions(language="zh")
        self.whisper_model = whisper.load_model("small", device=device)
        # whisper_model = whisper.load_model("medium", device=device)
        logger.info(f'Whisper model is loaded.')


    def _running(self):
        while self.is_running():
            if self.wave_queue.empty():
                time.sleep(.1)
                continue
            try:
                wave_path = self.wave_queue.get()
                logger.debug(f'transcribe path:{wave_path}')
                result = self.whisper_model.transcribe(wave_path)
                # transcribed_text = str(result["text"].encode('utf-8'))[2:-1].strip()
                transcribed_text = result["text"]
                # print(f'running addr: {self._config.mqtt_address}')
                self.publish("hearing.trans.text", transcribed_text)        
                logger.info(f">>> \033[33m{transcribed_text}\033[0m")
                if os.path.exists(wave_path):
                    os.remove(wave_path)
                logger.debug(f'Remained waves: {self.wave_queue.qsize()}')
            except queue.Empty:
                pass
            except UnicodeEncodeError:
                logger.info(f">>> \033[33m{transcribed_text.encode('utf-8')}\033[0m")
            except Exception as ex:
                _, exc_value, _ = sys.exc_info()
                logger.error(exc_value)
