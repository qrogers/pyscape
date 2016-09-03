import curses
from math import ceil
from random import randint

#TODO: Implement run

class CombatHandler():
    def __init__(self, var_handler):
        self.var_handler = var_handler

        self.combat = False
        self.enemy = None
        self.commands= ["attack", "cast", "run", "drink", "look", "examine", "list", "exit"]

    def start_combat(self, unit):
        attacker = unit
        self.enemy = attacker
        status = self.var_handler.get('status_handler')
        io = self.var_handler.get('io_handler')
        command_processor = self.var_handler.get('command_processor')
        player = self.var_handler.get('player')
        hud = self.var_handler.get('hud_handler')
        self.combat = True
        io.output("You enter combat with a {0}".format(attacker.display_name), curses.color_pair(2))
        status.end_sequence()
        status.output("You are attacked by: {0}".format(attacker.display_name))
        hud.text_update()
        while self.combat:
            curses.curs_set(1)
            input = io.get_input(">>>>>>>:", curses.color_pair(2))
            if input.split(" ")[0] in self.commands:
                if "attack" in input:
                    output = self.attack(player, attacker)
                elif input == "run":
                    output = self.run(attacker)
                elif input.split(" ")[0] == "cast":
                    output = self.cast(input.split(" ")[1])
                else:
                    output = command_processor.receive_command(input)
                if attacker.state == "dead":
                    self.combat = False
                    self.enemy = None
                    output = (output[0] + "\nYou kill the {0}".format(attacker.display_name), output[1])
            else:
                output = ("You can't do that in combat", curses.color_pair(2))
            io.output(output[0], output[1])
            hud.text_update()
        status.start_sequence()

    def attack(self, player, enemy):
        player_accuracy = (ceil(player.attack_current / 2.0) + player.proficiency_current) - (ceil(enemy.defense_current / 2.0) + enemy.proficiency_current)
        if player_accuracy < -10:
            player_accuracy = -10
        elif player_accuracy > 10:
            player_accuracy = 10
        player_accuracy = int(player_accuracy * 5) + 85 + randint(0, 5)
        enemy_accuracy  = (ceil(enemy.attack_current / 2.0) + enemy.proficiency_current) - (ceil(player.defense_current / 2.0) + player.proficiency_current)
        if enemy_accuracy < -10:
            enemy_accuracy = -10
        elif enemy_accuracy > 10:
            enemy_accuracy = 10
        enemy_accuracy = int(enemy_accuracy * 5) + 85 + randint(0, 5)
        player_damage = 0
        enemy_damage = 0
        state = "miss"
        if randint(0, 100) <= player_accuracy:
            player_damage = player.attack_current - int(enemy.defense_current * 0.65)
            if player_damage < 0:
                player_damage = 0
            state = enemy.take_damage(player_damage)
        if state == "alive" or state == "miss":
            if randint(0, 100) <= enemy_accuracy:
                enemy_damage = enemy.attack_current - int(player.defense_current * 0.65)
                if enemy_damage < 0:
                    enemy_damage = 0
                player.take_damage(enemy_damage)
            return ("You attack, dealing {0} damage and taking {1} damage".format(player_damage, enemy_damage), curses.color_pair(2))
        elif state == "miss":
            return ("You miss and take {0}".format(enemy_damage), curses.color_pair(2))
        elif state == "dead":
            return ("You attack, dealing {0} damage".format(player_damage), curses.color_pair(2))
        else:
            raise ValueError("Unit is not alive or dead")

    def cast(self, spell):
        return (self.var_handler.get('spell_handler').cast(spell, self.enemy), curses.color_pair(2))

    def run(self, attacker):
        raise NotImplementedError("Not implemented: run")
