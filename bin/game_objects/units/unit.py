import yaml
from abc import ABCMeta, abstractmethod
from bin.game_objects.game_object import GameObject

stats_file = 'conf/game_objects/units/'

class Unit(GameObject):
    __metaclass__ = ABCMeta

    def __init__(self, number, area, name):
        self.stats = self._load_stats(self.__class__.__name__.lower())
        super(Unit, self).__init__(number, area, name, self.stats['description'])
        self.health_level = self.stats['health']
        self.attack_level = self.stats['attack']
        self.defense_level = self.stats['defense']
        self.proficiency_level = self.stats['proficiency']
        self.aggression = self.stats['aggression']
        self.drops = self.stats['drops']
        self.xp = self.stats['xp']
        self.health_current = self.health_level
        self.attack_current = self.attack_level
        self.defense_current = self.defense_level
        self.proficiency_current = self.proficiency_level

        # Set to unit_handler.kill() by unit_handler
        self.die = None

        self.area = area
        self.location = self.area.location

        self.in_combat = False
        self.state = "alive"

    def _load_stats(self, name):
        return yaml.load(open(stats_file + name + ".yaml"))

    def take_damage(self, damage):
        self.health_current -= damage
        if self.health_current <= 0:
            self.die(self)
            self.state = "dead"
        return self.state

    def get_name(self):
        return self.display_name

    def get_status(self):
        return "Health: {0}/{1}".format(self.health_current, self.health_level)

    def set_combat(self, in_combat):
        self.in_combat = in_combat
