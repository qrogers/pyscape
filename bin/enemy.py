from abc import ABCMeta

from game_objects.units.unit import Unit


class Enemy(Unit):
    __metaclass__ = ABCMeta

    def die(self):
        pass
        #self.area.var_handler.get('io_handler').output(self.class_name + " has died")