# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from holon.HolonicAgent import HolonicAgent
from dialog.nlu import Nlu

class DialogSystem(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.body_agents.append(Nlu(cfg))
