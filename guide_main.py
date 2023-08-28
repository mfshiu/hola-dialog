import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from holon import config
from holon.HolonicAgent import HolonicAgent

from hearing import Hearing
from voice import Voice
from brain import Brain
from dialog import DialogSystem

class GuideMain(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.body_agents.append(DialogSystem(cfg))
        self.head_agents.append(Hearing(cfg))
        self.body_agents.append(Brain(cfg))
        self.head_agents.append(Voice(cfg))


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("guide.hearing.heared_text")
        client.subscribe("dialog.nlu.triplet")

        super()._on_connect(client, userdata, flags, rc)


    def _on_topic(self, topic, data):
        if "guide.hearing.heared_text" == topic:
            if '系統關機' in data:
                self.terminate()

        super()._on_topic(topic, data)
