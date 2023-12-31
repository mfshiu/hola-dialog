import os
from datetime import datetime as dt

from TTS.api import TTS

import helper
import app_config
from holon.HolonicAgent import HolonicAgent
from voice.speaker import Speaker


logger = helper.get_logger()


class ConquiVoice(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.head_agents.append(Speaker(cfg))


    def _on_connect(self):
        self._subscribe("voice.text")

        self.models = TTS.list_models()
        # logger.debug(f"TTS models: {self.models}")
        # self.tts = TTS(model_name=self.models[7], gpu=True)
        self.tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", gpu=True)

        super()._on_connect()


    def _on_message(self, topic:str, payload):
        data = self._convert_to_text(payload)

        if "voice.text" == topic:

            filename = dt.now().strftime(f"speak-%m%d-%H%M-%S.wav")
            filepath = os.path.join(app_config.output_dir, filename)
            logger.debug(f"speak_path:{filepath}")
            try:
                self.tts.tts_to_file(text=data, file_path=filepath)
                with open(filepath, "rb") as file:
                    file_content = file.read()
                os.remove(filepath)
                self._publish("voice.wave", file_content)
            except Exception as ex:
                logger.exception(ex)


'''
tts --list_models

TTS models: ['tts_models/multilingual/multi-dataset/your_tts', 'tts_models/multilingual/multi-dataset/bark', 'tts_models/bg/cv/vits', 'tts_models/cs/cv/vits', 'tts_models/da/cv/vits', 'tts_models/et/cv/vits', 'tts_models/ga/cv/vits', 'tts_models/en/ek1/tacotron2', 'tts_models/en/ljspeech/tacotron2-DDC', 'tts_models/en/ljspeech/tacotron2-DDC_ph', 'tts_models/en/ljspeech/glow-tts', 'tts_models/en/ljspeech/speedy-speech', 'tts_models/en/ljspeech/tacotron2-DCA', 'tts_models/en/ljspeech/vits', 'tts_models/en/ljspeech/vits--neon', 'tts_models/en/ljspeech/fast_pitch', 'tts_models/en/ljspeech/overflow', 'tts_models/en/ljspeech/neural_hmm', 'tts_models/en/vctk/vits', 'tts_models/en/vctk/fast_pitch', 'tts_models/en/sam/tacotron-DDC', 'tts_models/en/blizzard2013/capacitron-t2-c50', 'tts_models/en/blizzard2013/capacitron-t2-c150_v2', 'tts_models/en/multi-dataset/tortoise-v2', 'tts_models/en/jenny/jenny', 'tts_models/es/mai/tacotron2-DDC', 'tts_models/es/css10/vits', 'tts_models/fr/mai/tacotron2-DDC', 'tts_models/fr/css10/vits', 'tts_models/uk/mai/glow-tts', 'tts_models/uk/mai/vits', 'tts_models/zh-CN/baker/tacotron2-DDC-GST', 'tts_models/nl/mai/tacotron2-DDC', 'tts_models/nl/css10/vits', 'tts_models/de/thorsten/tacotron2-DCA', 'tts_models/de/thorsten/vits', 'tts_models/de/thorsten/tacotron2-DDC', 'tts_models/de/css10/vits-neon', 'tts_models/ja/kokoro/tacotron2-DDC', 'tts_models/tr/common-voice/glow-tts', 'tts_models/it/mai_female/glow-tts', 'tts_models/it/mai_female/vits', 'tts_models/it/mai_male/glow-tts', 'tts_models/it/mai_male/vits', 'tts_models/ewe/openbible/vits', 'tts_models/hau/openbible/vits', 'tts_models/lin/openbible/vits', 'tts_models/tw_akuapem/openbible/vits', 'tts_models/tw_asante/openbible/vits', 'tts_models/yor/openbible/vits', 'tts_models/hu/css10/vits', 'tts_models/el/cv/vits', 'tts_models/fi/css10/vits', 'tts_models/hr/cv/vits', 'tts_models/lt/cv/vits', 'tts_models/lv/cv/vits', 'tts_models/mt/cv/vits', 'tts_models/pl/mai_female/vits', 'tts_models/pt/cv/vits', 'tts_models/ro/cv/vits', 'tts_models/sk/cv/vits', 'tts_models/sl/cv/vits', 'tts_models/sv/cv/vits', 'tts_models/ca/custom/vits', 'tts_models/fa/custom/glow-tts', 'tts_models/bn/custom/vits-male', 'tts_models/bn/custom/vits-female']
'''