from bin.game_objects.game_object import GameObject

class Station(GameObject):
    def __init__(self, number, area, name, description):
        super(Station, self).__init__(number, area, name, description)