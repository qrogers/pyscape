import curses
import curses.panel
import sys

from command_processor import CommandProcessor
from io_handler import IOHandler
from hud_handler import HUDHandler
from game_objects.units.player import Player
from location_handler import LocationHandler
from inventory_handler import InventoryHandler
from time_handler import TimeHandler
from status_handler import StatusHandler
from combat_handler import CombatHandler
from spell_handler import SpellHander

#TODO: Tests
#TODO: Complain if window is too small
#TODO: Tab completion of args

class VarHandler():

    def __init__(self):
        self.vars = {}

    def bind(self, name, value):
        self.vars[name] = value

    def get(self, name):
        return self.vars[name]

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
    def get_text(self):
        return '\n'.join(self.text.split('\n'))

def curses_wrap():
    curses.wrapper(main)

def main(stdscr):

    holdstdout = StdOutWrapper()
    sys.stdout = holdstdout
    sys.stderr = holdstdout

    #stdscr = curses.initscr()

    screen_size = stdscr.getmaxyx()
    height = screen_size[0]
    width = screen_size[1]
    hincrement = int(height / 3)
    wincrement = int(width / 3)
    upper_left = (0, 0)
    upper_middle = (0, wincrement)
    upper_right = (0, 2 * wincrement)
    middle_left = (hincrement, 0)
    middle_middle = (hincrement, wincrement)
    middle_right = (hincrement, 2 * wincrement)
    lower_left = (2 * hincrement, 0)
    lower_middle = (2 * hincrement, wincrement)
    #lower_right= (2 * hincrement, 2 * wincrement)

    # Loadout   | HUD      | Skills
    # World Map | Spells   | Inventory
    # Terminal  | Status   | Inventory

    terwin = curses.newwin(hincrement, wincrement, lower_left[0], lower_left[1])
    terwin.box()
    ter_panel = curses.panel.new_panel(terwin)
    ter_panel.top()

    hudwin = curses.newwin(hincrement, wincrement, middle_left[0], middle_left[1])
    hudwin.box()
    hud_panel = curses.panel.new_panel(hudwin)
    hud_panel.top()

    invwin = curses.newwin(hincrement * 2, wincrement, middle_right[0], middle_right[1])
    invwin.box()
    inv_panel = curses.panel.new_panel(invwin)
    inv_panel.top()

    stswin = curses.newwin(hincrement, wincrement, lower_middle[0], lower_middle[1])
    stswin.box()
    sts_panel = curses.panel.new_panel(stswin)
    sts_panel.top()

    sklwin = curses.newwin(hincrement, wincrement, upper_left[0], upper_left[1])
    sklwin.box()
    skl_panel = curses.panel.new_panel(sklwin)
    skl_panel.top()

    eqpwin = curses.newwin(hincrement, wincrement, upper_right[0], upper_right[1])
    eqpwin.box()
    eqp_panel = curses.panel.new_panel(eqpwin)
    eqp_panel.top()

    mapwin = curses.newwin(hincrement, wincrement, middle_middle[0], middle_middle[1])
    mapwin.box()
    map_panel = curses.panel.new_panel(mapwin)
    map_panel.top()

    splwin = curses.newwin(hincrement, wincrement, upper_middle[0], upper_middle[1])
    splwin.box()
    spl_panel = curses.panel.new_panel(splwin)
    spl_panel.top()

    curses.start_color()

    #Terminal green
    curses.init_pair(1, 46, curses.COLOR_BLACK)
    #Dull red
    curses.init_pair(2, 9, curses.COLOR_BLACK)
    #Dull Teal
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    #Black on Grey
    curses.init_pair(4, curses.COLOR_BLACK, 244)
    #bronze
    curses.init_pair(5, 208, curses.COLOR_BLACK)
    curses.init_pair(6, 208, 130)
    #steel
    curses.init_pair(7, 252, curses.COLOR_BLACK)
    curses.init_pair(8, 253, 247)
    #mithril
    curses.init_pair(9, 117, curses.COLOR_BLACK)
    curses.init_pair(10, 117, 33)

    #Gold
    curses.init_pair(253, 220, curses.COLOR_BLACK)
    #White
    curses.init_pair(254, 255, curses.COLOR_BLACK)
    #Box color, dull grey
    curses.init_pair(255, 240, curses.COLOR_BLACK)

    curses.cbreak()
    curses.noecho()
    terwin.keypad(1)
    terwin.idcok(False)

    try:

        var_handler = VarHandler()

        command_processor = CommandProcessor(var_handler)
        var_handler.bind('command_processor', command_processor)

        io_handler = IOHandler(terwin, var_handler)
        var_handler.bind('io_handler', io_handler)

        hud_handler = HUDHandler(hudwin, var_handler)
        var_handler.bind('hud_handler', hud_handler)

        status_handler = StatusHandler(stswin)
        var_handler.bind('status_handler', status_handler)

        player = Player(sklwin, var_handler)
        var_handler.bind('player', player)

        inventory_handler = InventoryHandler(invwin, eqpwin, var_handler)
        var_handler.bind('inventory_handler', inventory_handler)

        location_handler = LocationHandler(mapwin, var_handler)
        var_handler.bind('location_handler', location_handler)

        time_handler = TimeHandler()
        var_handler.bind('time_handler', time_handler)

        spell_handler = SpellHander(splwin, var_handler)
        var_handler.bind('spell_handler', spell_handler)

        combat_handler = CombatHandler(var_handler)
        var_handler.bind('combat_handler', combat_handler)

        start = location_handler.spawn_location('entervale')
        location_handler.spawn_location('forest')
        start.move("mine")

        io_handler.output("Welcome to pyscape", curses.color_pair(3), curses.A_BOLD)
        hud_handler.text_update()
        hud_panel.top()
        inventory_handler.update_inv_window()
        curses.panel.update_panels()

        while True:
            curses.curs_set(1)
            input = io_handler.get_input("~~~~~~~:", curses.color_pair(1))
            output = command_processor.receive_command(input)
            io_handler.output(output[0], output[1])
            hud_handler.text_update()
            hud_panel.top()
            inventory_handler.update_inv_window()
            curses.panel.update_panels()

    except KeyboardInterrupt:
        terwin.addstr("exiting")
        exit(0)

    finally:
        terwin.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.write(holdstdout.get_text())
