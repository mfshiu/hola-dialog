import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
from logging.handlers import TimedRotatingFileHandler
import signal

from holon import config
from holon.HolonicAgent import HolonicAgent

# from visual.Visual import Visual
from hearing import Hearing
from voice import Voice
# from navi import Navigator
# from brain.navi import Navigator
from brain import Brain
from dialog import DialogSystem
import guide_config

class GuideMain(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.body_agents.append(DialogSystem(cfg))
        # self.head_agents.append(Visual())
        self.head_agents.append(Hearing(cfg))
        self.head_agents.append(Voice(cfg))
        # self.body_agents.append(Navigator(cfg))
        self.body_agents.append(Brain(cfg))


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("guide.hearing.heared_text")
        client.subscribe("dialog.nlu.triplet")

        super()._on_connect(client, userdata, flags, rc)


    def _on_topic(self, topic, data):
        if "guide.hearing.heared_text" == topic:
            if '系統關機' in data:
                self.terminate()
        # elif "dialog.nlu.triplet" == topic:
        #     logging.info(f'### {data} ###')

        super()._on_topic(topic, data)
