from abc import ABCMeta
from bin.game_objects.game_object import GameObject

class Place(GameObject):
    __metaclass__ = ABCMeta

    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Place, self).__init__(number, area, name, description)
        #Compared to player skill level to determine rewards
        self.difficulty = difficulty
        #Level required to gain resources
        self.level = level
        #Dict of place specific configurations
        self.info = info