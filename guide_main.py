import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from holon.HolonicAgent import HolonicAgent

from hearing import Hearing
import helper
from voice.conqui_voice import ConquiVoice
from voice.playht_voice import PlayHTVoice
from voice.playht_voice_v1 import PlayHTVoiceV1
from brain import Brain
from dialog import DialogSystem


logger = helper.get_logger()


class GuideMain(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        self.body_agents.append(DialogSystem(cfg))
        self.head_agents.append(Hearing(cfg))
        self.body_agents.append(Brain(cfg))
        self.head_agents.append(PlayHTVoiceV1(cfg))

        logger.debug(f"Init GuideMain done.")


    def _on_connect(self):
        self._subscribe("guide.hearing.heared_text")
        self._subscribe("dialog.nlu.triplet")

        logger.debug(f"Connect MQTT done.")
        super()._on_connect()
