import helper
from holon.HolonicAgent import HolonicAgent
from dialog.nlu.chatgpt_nlu import ChatGptNlu
# from dialog.nlu.llama_nlu import LlamaNlu


logger = helper.get_logger()

 
class Nlu(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.body_agents.append(ChatGptNlu(cfg))
        # self.body_agents.append(LlamaNlu(cfg))

        self.last_sentence = ""


    def _on_connect(self):
        self._subscribe("hearing.trans.text")
        self._subscribe("nlu.understand.knowledge")
        
        super()._on_connect()


    def _on_message(self, topic:str, payload):
        data = payload.decode('utf-8', 'ignore')
        
        if "hearing.trans.text" == topic:
            logger.debug(f"{self.name} heared '{data}'")
            self._publish("nlu.understand.text", str((data, self.last_sentence)))
        elif "nlu.understand.knowledge" == topic:
            self._publish("dialog.knowledge", data)
            logger.info(f"Understand: {data}")
