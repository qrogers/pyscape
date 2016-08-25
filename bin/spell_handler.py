import curses
import yaml

from math import floor

from bin.buff import Buff

class SpellHander():
    def __init__(self, splwin, var_handler):
        self.time   = var_handler.get('time_handler')
        self.player = var_handler.get('player')
        self.window = splwin
        self.spells = self.Spells()
        self.buffs = []
        self.update_window()

    def cast(self, spell, enemy=None):
        try:
            cast_spell = self.spells.spells[spell]
            if self.player.magic_level < cast_spell['level']:
                return "You do not have the level needed to cast that"
            elif self.player.magic_current < cast_spell['cost']:
                return "You do not have enough mana to cast that"
            else:
                if cast_spell['combat']:
                    if enemy is None:
                        return "That is a spell that can only be cast in combat"
                    else:
                        enemy.take_damage(floor(cast_spell['damage'] * (1 + (int(self.player.magic_current) / 100))))
                self.player.magic_current -= cast_spell['cost']
                self.update_window()
                for buff in self.player.buffs:
                    if spell.upper() == buff.name:
                        break
                else:
                    for buff in cast_spell['stats']:
                        spell_buff = Buff(spell.upper(), buff.keys()[0], buff[buff.keys()[0]], cast_spell['duration'], self.player, self.time)
                        self.player.add_buff(spell_buff)
                        self.buffs.append(spell_buff.name)
                if cast_spell['effect']:
                    self.spells.effects[spell]()
                self.update_window()
                return "You cast {0}".format(spell.upper())
        except AttributeError:
            return "That is not a spell"

    # def combat_cast(self, spell, enemy):
    #     pass

    def update_window(self):
        self.window.move(1,1)
        self.player.update_skill_window()
        maxyx = self.window.getmaxyx()
        spells = self.spells.spells

        for x in range(maxyx[1]):
            self.window.addch("_")
        self.window.move(1,int(maxyx[1] / 2) - 4)
        self.window.addstr("-Spells-")
        self.window.move(2,(maxyx[1] / 2) - (maxyx[1] / 3))
        self.window.addstr("Combat")
        self.window.move(2,(maxyx[1] / 2) + (maxyx[1] / 3) - 8)
        self.window.addstr("Utility")
        combat_spell_map = [
            ["FIR", "STN", "FIR", "FIR", "FIR"],
            ["FIR", "FIR", "FIR", "FIR", "FIR"],
            ["FIR", "FIR", "FIR", "FIR", "FIR"]
        ]
        utility_spell_map = [
            ["FIR", "FIR", "FIR", "FIR", "FIR"],
            ["FIR", "FIR", "FIR", "FIR", "FIR"],
            ["FIR", "FIR", "FIR", "FIR", "FIR"]
        ]
        i = 4
        j = 3
        for line in combat_spell_map:
            for spell in line:
                self.window.move(i, j)
                color = 3 if spells[spell.lower()]['cost']  > self.player.magic_current else 0
                color = 4 if spells[spell.lower()]['level'] > self.player.magic_level   else color
                self.window.addstr(spell, curses.color_pair(color))
                j += 6
                if j > 32:
                    i += 2
                    j = 3
        i = 4
        j = 38
        for line in utility_spell_map:
            for spell in line:
                self.window.move(i, j)
                color = 3 if spells[spell.lower()]['cost'] > self.player.magic_current else 0
                self.window.addstr(spell, curses.color_pair(color))
                j += 6
                if j > 64:
                    i += 2
                    j = 38
        self.window.move(10,1)
        for x in range(maxyx[1]):
            self.window.addch("_")
        self.window.move(10,int(maxyx[1] / 2) - 5)
        self.window.addstr("-Abilities-")
        self.window.move(12,4)
        self.window.addstr("\\.|./")
        self.window.move(13,4)
        self.window.addstr("<-O->")
        self.window.move(14,4)
        self.window.addstr(" /.\\ ")
        self.window.move(15,2)
        self.window.addstr("Overcharge")
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.attroff(curses.color_pair(255))

    class Spells():
        def __init__(self):
            self.spells = yaml.load(open("conf/spells.yaml"))
            self.effects = {"fir" : self.FIR}

        def FIR(self):
            print "FIR"
