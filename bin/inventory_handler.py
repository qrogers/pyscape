#-*- coding: UTF-8 -*-

from bin.item import Item
from bin.buff import Buff
import curses

#TODO: Add bank

class InventoryHandler:
    def __init__(self, inv_window, eqp_window, var_handler):
        self.inv_window = inv_window
        self.eqp_window = eqp_window
        self.var_handler = var_handler
        self.items = []
        self.gold = 0
        self.items.append(Item("materials", "bars", "steel_bar"))
        self.items.append(Item("materials", "bars", "bronze_bar"))
        self.items.append(Item("materials", "bars", "mithril_bar"))
        #self.items.append(Item("resources", "logs", "oak_log"))
        # self.items.append(Item("resources", "ores", "iron_ore"))
        # self.items.append(Item("resources", "ores", "iron_ore"))
        # self.items.append(Item("resources", "ores", "iron_ore"))
        # self.items.append(Item("resources", "ores", "iron_ore"))
        # self.items.append(Item("resources", "ores", "iron_ore"))
        # self.items.append(Item("resources", "ores", "copper_ore"))
        # self.items.append(Item("resources", "ores", "copper_ore"))
        # self.items.append(Item("resources", "ores", "copper_ore"))
        # self.items.append(Item("resources", "ores", "copper_ore"))
        # self.items.append(Item("gear", "chests", "bronze_chest"))
        # self.items.append(Item("gear", "legs", "bronze_legs"))
        # self.items.append(Item("gear", "gloves", "leather_gloves"))
        self.items.append(Item("gear", "helmets", "steel_helmet"))
        self.items.append(Item("gear", "helmets", "bronze_helmet"))
        # self.items.append(Item("gear", "capes", "bronze_cape"))
        # self.items.append(Item("gear", "offhands", "leather_shield"))
        # self.items.append(Item("gear", "weapons", "bronze_spear"))
        # self.items.append(Item("gear", "boots", "leather_boots"))
        # self.items.append(Item("materials", "energy", "mystic_energy"))
        # self.items.append(Item("materials", "energy", "mystic_energy"))
        # self.items.append(Item("materials", "energy", "mystic_energy"))
        # self.items.append(Item("materials", "energy", "mystic_energy"))
        # self.items.append(Item("consumables", "potions", "heal_potion"))
        # self.items.append(Item("consumables", "enchantments", "burning_aura"))
        # self.items.append(Item("consumables", "enchantments", "burning_aura"))
        # self.bronze_cape = Item("gear", "capes", "bronze_cape")
        # self.items.append(self.bronze_cape)
        # self.bronze_boot = Item("gear", "boots", "bronze_boots")
        # self.items.append(self.bronze_boot)
        # self.bronze_leg = Item("gear", "legs", "bronze_legs")
        # self.items.append(self.bronze_leg)
        # self.bronze_chest = Item("gear", "chests", "bronze_chest")
        # self.items.append(self.bronze_chest)
        # self.bronze_helmet = Item("gear", "helmets", "bronze_helmet")
        # self.items.append(self.bronze_helmet)

        self.dropped = []

        self.equipped = {"helmet" : None, "chest" : None, "offhand" : None, "ring" : None, "glove" : None, "boot" : None,
                         "cape" : None, "weapon": None, "leg" : None}

        self.max_items = 42

        self.frames = {}

        self.num_columns = 6

        self.ore_frame              = ["'''''''''", [":",":"], [":",":"], "........."]
        self.bar_frame              = ["---------", ["|","|"], ["|","|"], "---------"]
        self.log_frame              = ["<><>^<><>", ["{","}"], ["{","}"], "<><>^<><>"]
        self.plank_frame            = ["=========", ["[","]"], ["[","]"], "========="]
        self.meat_frame             = ["~`~`~`~`~", ["$","$"], ["$","$"], "~`~`~`~`~"]
        self.food_frame             = ["%%%%%%%%%", ["*","*"], ["*","*"], "%%%%%%%%%"]
        self.hide_frame             = ["TTTTTTTTT", ["#","#"], ["#","#"], "TTTTTTTTT"]
        self.leather_frame          = ["~~~~~~~~~", ["$","$"], ["$","$"], "~~~~~~~~~"]
        self.plant_frame            = ["WWWWWWWWW", ["W","M"], ["W","M"], "MMMMMMMMM"]
        self.ingredient_frame       = ["888888888", ["8","8"], ["8","8"], "888888888"]
        self.fiber_frame            = ["-~-~-~-~-", ["H","H"], ["H","H"], "~-~-~-~-~"]
        self.cloth_frame            = ["ZZZZZZZZZ", ["(",")"], ["(",")"], "ZZZZZZZZZ"]
        self.weapon_frame           = ["<><>^<><>", ["<",">"], ["<",">"], "<><>^<><>"]
        self.offhand_frame          = ["<><>^<><>", ["<",">"], ["<",">"], "<><>^<><>"]
        self.cape_frame             = [".........", [":",":"], [":",":"], "........."]
        self.chest_frame            = [".........", [":",":"], [":",":"], "........."]
        self.glove_frame            = ["OOOOOOOOO", ["X","X"], ["X","X"], "OOOOOOOOO"]
        self.boot_frame             = ["MMMMMMMMM", ["<",">"], ["<",">"], "WWWWWWWWW"]
        self.leg_frame              = ["HHHHHHHHH", ["!","!"], ["!","!"], "HHHHHHHHH"]
        self.helmet_frame           = ["HHHHHHHHH", ["!","!"], ["!","!"], "HHHHHHHHH"]
        self.potion_frame           = ["         ", [" "," "], [" "," "], "         "]
        self.energy_frame           = ["*~*~*~*~*", [" "," "], [" "," "], "*~*~*~*~*"]
        self.enchantment_frame      = ["         ", [" "," "], [" "," "], "         "]

        self.steel_sword_frame       = ["LI       ",
                                      [" ",    " "],
                                      [" ",    " "],
                                       " |       "]

        self.bronze_spear_frame     = ["|        ",
                                      ["|",    " "],
                                      ["|",    " "],
                                       "V        "]

        self.frames["ore"]          = self.ore_frame
        self.frames["bar"]          = self.bar_frame
        self.frames["log"]          = self.log_frame
        self.frames["meat"]         = self.meat_frame
        self.frames['food']         = self.food_frame
        self.frames["hide"]         = self.hide_frame
        self.frames["leather"]      = self.leather_frame
        self.frames["plank"]        = self.plank_frame
        self.frames["plant"]        = self.plant_frame
        self.frames["ingredient"]   = self.ingredient_frame
        self.frames["fiber"]        = self.fiber_frame
        self.frames["cloth"]        = self.cloth_frame
        self.frames["weapon"]       = self.weapon_frame
        self.frames["offhand"]      = self.offhand_frame
        self.frames["cape"]         = self.cape_frame
        self.frames["chest"]        = self.chest_frame
        self.frames["glove"]        = self.glove_frame
        self.frames["boot"]         = self.boot_frame
        self.frames["leg"]          = self.leg_frame
        self.frames["helmet"]       = self.helmet_frame
        self.frames["potion"]       = self.potion_frame
        self.frames["energy"]       = self.energy_frame
        self.frames["enchantment"]  = self.enchantment_frame

        self.frames["steel_sword"]   = self.steel_sword_frame
        self.frames["bronze_spear"] = self.bronze_spear_frame

        self.update_eqp_window()

    class InventoryFullException(Exception):
        pass

    def change_gold(self, amount):
        self.gold += int(amount)
        self.update_inv_window()

    def add_item(self, category, type, name, quantity=1):
        i = quantity
        capacity = False
        while i > 0:
            new_item = Item(category, type, name)
            if len(self.items) < self.max_items:
                self.items.append(new_item)
            else:
                self.dropped.append(new_item)
                capacity = True
            i -= 1
        if capacity:
            self.var_handler.get('status_handler').output("You do have enough room in your inventory\nExcess items have been dropped", curses.color_pair(2))
        self.update_inv_window()

    def remove_item(self, item):
        self.items.remove(item)

    def take(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            self.dropped.remove(item)
            return 0
        else:
            return 1

    def drop(self, item):
        self.remove_item(item)
        self.dropped.append(item)

    def organize(self):
        self.items.sort(key=lambda item: [item.category, item.type, item.tier])

    def update_inv_window(self):
        self.inv_window.erase()
        self.organize()
        i = 0
        while i < len(self.items):
            self.draw((i / self.num_columns) + 1, i % self.num_columns, self.items[i])
            i += 1
        self.inv_window.move(self.inv_window.getmaxyx()[0] - 2, 2)
        self.inv_window.addstr("Gold: {0}".format(self.gold), curses.color_pair(253))
        self.inv_window.attron(curses.color_pair(255))
        self.inv_window.box()
        self.inv_window.attroff(curses.color_pair(255))
        self.inv_window.refresh()

    def equip(self, item):
        if self.equipped[item.type] is not None:
            self.drop(item)
            self.unequip(self.equipped[item.type])
            self.take(item)
        self.equipped[item.type] = item
        player = self.var_handler.get('player')
        time = self.var_handler.get('time_handler')
        for buff in item.stats:
            buff = Buff(item.name, buff.keys()[0], buff[buff.keys()[0]], -1, player, time)
            player.add_buff(buff)
            item.buffs.append(buff)
        self.remove_item(item)
        self.update_eqp_window()

    def unequip(self, item):
        self.equipped[item.type] = None
        self.items.append(item)
        player = self.var_handler.get('player')
        for buff in item.buffs:
            player.remove_buff(buff)
        item.buffs = []
        self.update_eqp_window()

    def update_eqp_window(self):
        x_third = int(self.eqp_window.getmaxyx()[1] / 3)
        y_third = int(self.eqp_window.getmaxyx()[0] / 3)
        self.eqp_window.erase()
        slots = [["cape", "helmet", "glove"],
                 ["weapon", "chest", "offhand"],
                 ["boot", "leg", "ring"]]
        i = 0
        for y_pos in [int(y_third * .25), int(y_third * 1.25), int(y_third * 2.25)]:
            j = 0
            for x_pos in [int(x_third * 0.3), int(x_third * 1.3), int(x_third * 2.3)]:
                slot = slots[i][j]
                item = self.equipped[slot]
                if item is not None:
                    image_0     = item.image[0]
                    image_1     = item.image[1]
                    image_2     = item.image[2]
                    name0       = item.name.split("_")[0]
                    name1       = item.name.split("_")[1]
                    image_color = item.frame_color
                    text_color  = item.text_color
                else:
                    image_0     = "      "
                    image_1     = "      "
                    image_2     = "      "
                    name0       = "none"
                    name1       = ""
                    image_color = curses.color_pair(255)
                    text_color  = curses.color_pair(255)
                self.eqp_window.move(y_pos + 0, x_pos)
                self.eqp_window.addstr("--------", curses.color_pair(255))
                self.eqp_window.move(y_pos + 1, x_pos)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(image_0,image_color)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(" " + slot + ":",  curses.color_pair(254))
                self.eqp_window.move(y_pos + 2, x_pos)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(image_1, image_color)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(" " + name0, text_color)
                self.eqp_window.move(y_pos + 3, x_pos)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(image_2, image_color)
                self.eqp_window.addch("|", curses.color_pair(255))
                self.eqp_window.addstr(" " + name1, text_color)
                self.eqp_window.move(y_pos + 4, x_pos)
                self.eqp_window.addstr("--------", curses.color_pair(255))
                j += 1
            i += 1
        self.eqp_window.attron(curses.color_pair(255))
        self.eqp_window.box()
        self.eqp_window.attroff(curses.color_pair(255))

    def in_inventory(self, name):
        for item in self.items:
            if item.name.replace("_", " ") == name or item.name == name:
                return item
        return None

    def free_spaces(self):
        return self.max_items - len(self.items)

    def draw(self, y, x, item):
        try:
            frame = self.frames[item.name]
        except KeyError:
            frame = self.frames[item.type]
        self.inv_window.move((y * 4) - 3, x * 10 + 2)
        self.inv_window.addstr(frame[0], item.frame_color)
        self.inv_window.move((y * 4) - 2, x * 10 + 2)
        self.inv_window.addstr(frame[1][0], item.frame_color)
        self.inv_window.addstr(item.display_name[0], item.text_color)
        self.inv_window.addstr(frame[1][1], item.frame_color)
        self.inv_window.move((y * 4) - 1, x * 10 + 2)
        self.inv_window.addstr(frame[2][0], item.frame_color)
        self.inv_window.addstr(item.display_name[1], item.text_color)
        self.inv_window.addstr(frame[2][1], item.frame_color)
        self.inv_window.move((y * 4) - 0, x * 10 + 2)
        self.inv_window.addstr(frame[3], item.frame_color)