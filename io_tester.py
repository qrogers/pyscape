import curses
import curses.ascii
import re

stdscr = curses.initscr()


curses.cbreak()
curses.noecho()
stdscr.keypad(1)
stdscr.idcok(False)

buffer = ''
commands = []
commands_index = -1

commands_list = ['start', 'stop', 'echo', 'test']

def set_line():
    stdscr.move(cursor[0], 0)
    stdscr.deleteln()
    stdscr.addstr(buffer)

try:
    while True:
            c = stdscr.getch()
            cursor = stdscr.getyx()
            #stdscr.addstr(str(c))

            #If tab is pressed, search through commands tht start with the current buffer and set the buffer to the first match
            if c == 9:
                match = None
                for command in commands_list:
                    matched = re.match(buffer, command)
                    if matched is not None:
                        match = command
                        break
                if match is not None:
                    buffer = match
                    set_line()
            if c == 10:
                stdscr.move(cursor[0], len(buffer))
                stdscr.addch(c)
                if len(buffer) > 0:
                    commands.insert(0, buffer)
                    commands_index = -1
                buffer = ''
            elif c == 127:
                if cursor[1] > 0:
                    buffer = buffer[:len(buffer) - 1]
                    stdscr.delch(cursor[0], cursor[1] - 1)
            elif c == curses.KEY_UP:
                if commands_index + 1 < len(commands):
                    if commands_index == -1 and len(buffer) > 0:
                        commands.insert(0, buffer)
                        commands_index += 1
                    commands_index += 1
                    buffer = commands[commands_index]
                    set_line()
            elif c == curses.KEY_DOWN:
                if commands_index - 1 >= 0:
                    commands_index -= 1
                    buffer = commands[commands_index]
                    set_line()
                elif commands_index == 0:
                    commands_index -= 1
                    buffer = ''
                    set_line()
            elif c == curses.KEY_LEFT:
                if cursor[1] > 0:
                    stdscr.move(cursor[0], cursor[1] - 1)
            elif c == curses.KEY_RIGHT:
                if cursor[1] < len(buffer):
                    stdscr.move(cursor[0], cursor[1] + 1)
            #echo and record all lowercase letters
            elif c >= 97 and c <= 122:
                char = curses.ascii.unctrl(c)
                if cursor[1] == len(buffer):
                    if len(buffer) + 1 > stdscr.getmaxyx()[1]:
                        stdscr.move(cursor[0] + 1, 0)
                    stdscr.addstr(char)
                else:
                    stdscr.insstr(char)
                    stdscr.move(cursor[0], cursor[1] + 1)
                buffer = buffer[:cursor[1]] + char + buffer[cursor[1]:]
except KeyboardInterrupt:
    exit(0)

finally:
    stdscr.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()