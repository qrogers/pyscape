import curses

class HUDHandler():
    def __init__(self, window, var_handler):
        self.window = window
        self.var_handler = var_handler
        self.text = [None] * 12
        self.color = curses.color_pair(0)
        self.style = curses.A_NORMAL

    def text_update(self):
        player = self.var_handler.get('player')
        buffs = player.buffs
        combat_handler = self.var_handler.get('combat_handler')
        self.text[0] = player.location.display_name + " - " + player.area.display_name
        self.text[1] = player.get_status()
        if combat_handler.enemy is not None:
            self.text[2] = "In combat with:"
            self.text[3] = combat_handler.enemy.display_name + " " + combat_handler.enemy.get_status()
        else:
            self.text[2] = "Not in combat"
            self.text[3] = ""
        self.text[4] = "Ticks: " + str(self.var_handler.get('time_handler').ticks)
        self.text[5] = "Moves: " + str(self.var_handler.get('time_handler').moves)
        self.text[6] = ""
        self.text[7] = "Combat Stats:"
        pna = "" if player.attack_current  < player.attack_level  else "+"
        pnd = "" if player.defense_current < player.defense_level else "+"
        pns = "" if player.stealth_current < player.stealth_level else "+"
        self.text[8] = "Attack {0}{1} Defense {2}{3} Stealth {4}{5}".format(pna, player.attack_current  - player.attack_level,
                                                                               pnd, player.defense_current - player.defense_level,
                                                                               pns, player.stealth_current - player.stealth_level)
        buff_string = ""
        for buff in buffs:
            if buff.duration > 0:
                buff_string += buff.display_name + " - " + str(buff.duration) + " "
        self.text[9] = ""
        self.text[10] = "Buffs:"
        self.text[11] = buff_string
        self._window_update()

    def _window_update(self):
        curses.curs_set(0)
        self.window.erase()
        self.window.move(1, 1)
        for line in self.text:
            location = self.window.getyx()
            self.window.addstr(line, self.color + self.style)
            self.window.move(location[0] + 1, location[1])
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.attroff(curses.color_pair(255))
        self.window.refresh()
