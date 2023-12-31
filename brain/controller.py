import ast

import helper
from holon.HolonicAgent import HolonicAgent


logger = helper.get_logger()


class Controller(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.active_subject = None
        self.registered_subjects = []


    def _on_connect(self):
        self._subscribe("dialog.knowledge")
        self._subscribe("brain.register_subject")
        self._subscribe("brain.unregister_subject")
        self._subscribe("brain.subject_done")
        super()._on_connect()


    def _on_message(self, topic:str, payload):
        data = self._convert_to_text(payload)
        
        if "dialog.knowledge" == topic:
            if self.active_subject:
                self._publish(f'{self.active_subject}.knowledge', data)
                # logger.warning(f"Active subject: {self.active_subject}")
            else:
                knowledge = ast.literal_eval(data)
                if (subject := knowledge[0][0]) in self.registered_subjects:
                    self.active_subject = subject
                    logger.info(f"Active subject: {self.active_subject}")
                    self._publish(f'{self.active_subject}.knowledge', data)
                else:
                    logger.warning(f"Uknown subject: {subject}")
        elif "brain.register_subject" == topic:
            if not data in self.registered_subjects:
                self.registered_subjects.append(data)
                logger.info(f"Register subject: {data}")
        elif "brain.unregister_subject" == topic:
            if data in self.registered_subjects:
                self.registered_subjects.remove(data)
                logger.info(f"Unregister subject: {data}")
        elif "brain.subject_done" == topic:
            logger.info(f"subject: {self.active_subject} is done.")
            self.active_subject = None
