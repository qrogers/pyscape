import curses
import curses.ascii
import re

class IOHandler():

    def __init__(self, window, var_handler):
        self.commands = []

        self.commands_list = var_handler.get('command_processor').command_dictionary


        self.window = window

        self.prompt_line = self.window.getmaxyx()[0] - 3

        self.history = []

    def set_line(self, cmd_buffer, prompt, color_style=1):
        self.window.move(self.window.getyx()[0], 1)
        self.window.deleteln()
        self.window.insertln()
        self.window.addstr(prompt + cmd_buffer, color_style)

    def get_input(self, prompt="", color_pair=1, style=1):
        cmd_buffer = ""

        color_style = color_pair + style

        commands_index = -1

        self.window.deleteln()
        self.window.insertln()
        self.set_line("", prompt, color_style)
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.attroff(curses.color_pair(255))

        while True:
            c = self.window.getch()
            cursor = self.window.getyx()

            if c == curses.KEY_RESIZE:
                pass
                #HANDLE RESIZE
            #Ctrl-a move cursor to start of line
            if c == 1:
                self.window.move(cursor[0], len(prompt) + 1)
            #Ctrl-E move cursor to end of line
            elif c == 5:
                self.window.move(cursor[0], len(prompt) + len(cmd_buffer) + 1)
            #Ctrl-u clear line
            elif c == 21:
                cmd_buffer = ""
                self.set_line(cmd_buffer, prompt, color_style)
            #If tab is pressed, search through commands tht start with the current cmd_buffer and set the cmd_buffer to the first match
            elif c == 9:
                match = None
                for command in self.commands_list:
                    matched = re.match(cmd_buffer, command)
                    if matched is not None:
                        match = command
                        break
                if match is not None:
                    cmd_buffer = match
                    self.set_line(cmd_buffer, prompt, color_style)
            #Enter, submit cmd_buffer
            elif c == 10:
                cmd_buffer = cmd_buffer.strip()
                if len(cmd_buffer) > 0:
                    if len(self.commands) <= 0:
                        self.commands.insert(0, cmd_buffer)
                    elif self.commands[0] != cmd_buffer:
                        self.commands.insert(0, cmd_buffer)
                    self.history.insert(0, (cmd_buffer, color_style))
                    return cmd_buffer
                else:
                    self.output("")
                    self.set_line("", prompt, color_style)
            #Backspace, delete previous char
            elif c == 127 or c == 263:
                if cursor[1] > len(prompt) + 1:
                    cmd_buffer = cmd_buffer[:cursor[1] - 2 - len(prompt)] + cmd_buffer[cursor[1] - 1 - len(prompt):]
                    self.set_line(cmd_buffer, prompt, color_style)
                    self.window.move(cursor[0], cursor[1] - 1)
            elif c == curses.KEY_UP:
                if commands_index + 1 < len(self.commands):
                    if commands_index == -1 and len(cmd_buffer) > 0:
                        self.commands.insert(0, cmd_buffer)
                        commands_index += 1
                    commands_index += 1
                    cmd_buffer = self.commands[commands_index]
                    self.set_line(cmd_buffer, prompt, color_style)
            elif c == curses.KEY_DOWN:
                if commands_index - 1 >= 0:
                    commands_index -= 1
                    cmd_buffer = self.commands[commands_index]
                    self.set_line(cmd_buffer, prompt, color_style)
                elif commands_index == 0:
                    commands_index -= 1
                    cmd_buffer = ''
                    self.set_line(cmd_buffer, prompt, color_style)
            elif c == curses.KEY_LEFT:
                if cursor[1] - 1 > len(prompt):
                    self.window.move(cursor[0], cursor[1] - 1)
            elif c == curses.KEY_RIGHT:
                if cursor[1] - len(prompt) - 1 < len(cmd_buffer):
                    self.window.move(cursor[0], cursor[1] + 1)
            #echo and record all lowercase letters
            elif (c >= 95 and c <= 122) or (c >= 48 and c <= 57) or c == 32:
                char = curses.ascii.unctrl(c)
                if cursor[1] + 3 > self.window.getmaxyx()[1]:
                         curses.flash()
                else:
                    if cursor[1] - len(prompt) - 1 == len(cmd_buffer):
                        self.window.addstr(char, color_style)
                        cmd_buffer = cmd_buffer[:cursor[1]] + char + cmd_buffer[cursor[1]:]
                    else:
                        self.window.insstr(char, color_style)
                        self.window.move(cursor[0], cursor[1] + 1)
                        cmd_buffer = cmd_buffer[:cursor[1] - len(prompt) - 1] + char + cmd_buffer[cursor[1] - len(prompt) - 1:]
            self.window.attron(curses.color_pair(255))
            self.window.box()
            self.window.attroff(curses.color_pair(255))

    def output(self, text, color_pair=1, style=curses.A_NORMAL):
        str_text = str(text)
        for line in str_text.split("\n"):
            if len(line) > self.window.getmaxyx()[1]:
                pass
                #str_text = str_text.replace(" ", "\n", 7)
                #raise ValueError("line is longer than window")
            self.history.insert(0, (line, color_pair + style))
            if len(self.history) > self.prompt_line:
                self.history.pop(self.prompt_line)
        num_lines = self.prompt_line
        self.window.move(self.window.getmaxyx()[0] - 3 - self.prompt_line, 1)
        while (num_lines >= 0):
            cursor = self.window.getyx()
            self.window.deleteln()
            self.window.insertln()
            if len(self.history) > num_lines:
                self.window.addstr(self.history[num_lines][0], self.history[num_lines][1])
            self.window.move(cursor[0] + 1, 1)
            num_lines -= 1
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.attroff(curses.color_pair(255))

    def clear_screen(self):
        self.history = []
        return ""
