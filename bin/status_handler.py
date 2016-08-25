import curses
import re

class StatusHandler():
    def __init__(self, window):
        self.window = window

        self.prompt_line = self.window.getmaxyx()[0] - 2

        self.history = []

        self.output("")

    def output(self, text, color_pair=1, style=curses.A_NORMAL):
        str_text = str(text).replace("_", " ")

        def a_rep(matchobj):
            return matchobj.group(0).replace("a", "an", 1)

        str_text = re.sub("a [aeiou]", a_rep, str_text)
        for line in str_text.split("\n"):
            self.history.insert(0, (line, color_pair + style))
            if len(self.history) > self.prompt_line:
                self.history.pop(self.prompt_line)
        num_lines = self.prompt_line
        self.window.move(self.window.getmaxyx()[0] - 2 - self.prompt_line, 1)
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
        self.window.refresh()

    def slow_output(self, text, time, color_pair=1, style=curses.A_NORMAL):
        str_text = str(text)
        self.history.insert(0, ("", color_pair + style))
        for char in str_text:
            self.history[0] = (self.history[0][0] + char, self.history[0][1])
            if len(self.history) > self.prompt_line:
                self.history.pop(self.prompt_line)
            num_lines = self.prompt_line
            self.window.move(self.window.getmaxyx()[0] - 2 - self.prompt_line, 1)
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
            self.window.refresh()
            if char == ",":
                time.sleep(.5)
            elif char == ".":
                time.sleep(1)
            elif char == " ":
                pass
            else:
                time.sleep(.05)
        time.sleep(.03)

    def start_sequence(self):
        curses.curs_set(0)

    def end_sequence(self):
        curses.curs_set(1)