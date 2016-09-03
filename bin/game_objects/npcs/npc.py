from abc import ABCMeta
from bin.game_objects.game_object import GameObject

class NPC(GameObject):
    __metaclass__ = ABCMeta

    def __init__(self, number, area, name, description):
        super(NPC, self).__init__(number, area, name, description)