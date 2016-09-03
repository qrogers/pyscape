from bin.game_objects.npcs.npc import NPC

class Bank(NPC):
    def __init__(self, number, area, name, description, info):
        super(Bank, self).__init__(number, area, name, description)