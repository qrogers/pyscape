import curses
import os
import yaml
from bin.buff import Buff

#TODO: Add stores

class Item():
    def __init__(self, category, type, name):
        if type == "*" or category == "*":
            for folder in os.listdir('conf/items'):
                for file in os.listdir('conf/items/{0}'.format(folder if category == "*" else category)):
                    try:
                        self.info = self._load_stats("conf/items/{0}/{1}/{2}.yaml".format(folder if category == "*" else category, file if type == "*" else type, name))
                        break
                    except IOError:
                        pass
        else:
            self.info = self._load_stats("conf/items/{0}/{1}/{2}.yaml".format(category, type, name))

        try:
            self.info
        except:
            raise ValueError("That item does not exist")

        self.name = self.info['name']
        self.display_name = self.info['display_name']
        self.category = self.info['category']
        self.type = self.info['type']
        self.tier = self.info['tier']
        self.examine = self.info['examine']
        self.text_color = curses.color_pair(self.info['text_color'])
        self.frame_color = curses.color_pair(self.info['frame_color'])
        if self.category == "gear" or self.category == "consumables":
            if self.category == "gear":
                self.image = self.info['image']
                self.enchantment = None
            if self.category == "consumables":
                self.duration = self.info['duration']
            self.stats = self.info['stats']
            # Buffs that the item gives from enchantments on it
            self.buffs = []

    def _load_stats(self, file):
        return yaml.load(open(file))

    def drink(self, player, time):
        if self.type != "potion":
            return 1
        else:
            for buff in player.buffs:
                if self.name == buff.name:
                    return 2
            time.tick(1)
            for buff in self.stats:
                player.add_buff(Buff(self.name, buff.keys()[0], buff[buff.keys()[0]], self.duration, player, time))
            return "You drink the {0}".format(self.name.replace("_", " "))