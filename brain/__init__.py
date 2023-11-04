from holon.HolonicAgent import HolonicAgent
from brain.navi import Navigator
from brain.greeting import Greeting
from brain.controller import Controller


class Brain(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.head_agents.append(Controller(cfg))
        self.body_agents.append(Navigator(cfg))
        self.body_agents.append(Greeting(cfg))        
