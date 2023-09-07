import ast
import os
import threading
import time

import helper
from holon.HolonicAgent import HolonicAgent
from brain import brain_helper
from dialog.nlu import chatgpt


logger = helper.get_logger()


class Greeting(HolonicAgent):
    def __init__(self, cfg):
        self.is_active = False
        super().__init__(cfg)


    def __set_active(self, active):
        self.is_active = active
        logger.info(f'Active: {self.is_active}')


    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("greeting.knowledge")
        client.subscribe("voice.spoken")

        self.__set_active(True)

        threading.Timer(1, lambda: self.publish('brain.register_subject', 'greeting')).start()
        super()._on_connect(client, userdata, flags, rc)


    def _on_topic(self, topic, data):
        if "greeting.knowledge" == topic:
            if self.is_active:
                self.__set_active(False)
                knowledge = ast.literal_eval(data)
                # logger.debug(f'Sentence: {knowledge[2][0]}')

                happy = (knowledge[0][1] == 'happy')
                response = chatgpt.response_greeting(user_greeting=knowledge[2][0], is_happy=happy)
                brain_helper.speak(self, response)

                self.publish('brain.subject_done')
            else:
                logger.warning(f'Waiting to finish speaking.')
        elif "voice.spoken":
            self.__set_active(True)


        super()._on_topic(topic, data)


    def terminate(self):
        self.publish('brain.unregister_subject', 'greeting')
        super().terminate()