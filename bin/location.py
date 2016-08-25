from bin.area import Area
import curses
import os
import yaml

class Location():
    def __init__(self, name, conf, window, var_handler):
        self.name = name
        self.display_name = name[:1].upper() + name[1:]
        self._conf = conf
        self.conf_dir = "conf/game_objects/locations/{0}/".format(name)
        self.window = window
        self.var_handler = var_handler
        self.areas = {}

        self.start_area = self._conf['start']

        self.colors = self._conf['colors']

        self.active = None

        self.map = []
        self.location_map = []
        for location in self._conf['points']:
            self.map.append(self._conf['points'][location])
            self.location_map.append(location)

        self.links = []

        self.connections = self._conf['map']

        for file in os.listdir(self.conf_dir):
            area = file.split(".")[0]
            if area != name and area != "area_map" and area != "color_map":
                self.areas[area] = Area(area, self, yaml.load(open(self.conf_dir + area + ".yaml")), var_handler)

        for location in self._conf['map']:
            for link in self._conf['map'][location]:
                self.links.append((self._conf['points'].keys().index(location), self._conf['points'].keys().index(link)))

        for link in self.links:
            if (link[1], link[0]) in self.links:
                self.links.remove((link[1], link[0]))

    def move(self, area):
        self.var_handler.get('time_handler').move()
        if self.active is not None:
            self.active.deactivate()
        self.active = self.areas[area]
        self.active.activate()
        self.var_handler.get('player').move_area(self.active)
        self.draw_location_map()
        self.draw_area_map()

    def travel(self, location):
        self.active.deactivate()
        self.active = None
        new_location = self.var_handler.get('location_handler').get_location(location)
        new_location.move(self.start_area)

    def draw_area_map(self):
        with open(self.conf_dir + "area_map", 'r') as area_map:
            draw_area = area_map.read()
        with open(self.conf_dir + "color_map", 'r') as color_map:
            color_area = color_map.read()

        color_area = list(color_area.replace("\n", ""))
        draw = []
        for line in draw_area.split("\n"):
            draw.append(line)

        offset = 31

        current = "*"

        self.window.move(2, offset)
        i = 0
        for line in draw:
            self.window.move(self.window.getyx()[0] + 1, offset)
            for ch in line:
                if ch == str(self.areas.keys().index(self.active.name)):
                    self.window.addch(current, curses.color_pair(254))
                else:
                    self.window.addch(ch, curses.color_pair(self.colors[color_area[i]]))
                i += 1

        self.window.move(1, offset + 2)
        for area in self.areas:
            if area == self.active.name:
                self.window.addstr(current + ":" + area + " ")
            else:
                self.window.addstr(str(self.areas.keys().index(area)) + ":" + area + " ")
            if self.window.getyx()[1] > 60:
                self.window.move(2, offset + 2)

    def draw_location_map(self):
        draw_location = [["/","\\"],
                         [],
                         [],
                         [],
                         [],
                         [],
                         [],
                         [],
                         [],
                         [],
                         ["\\","/"]]

        width = 30

        for y in range(1, len(draw_location) - 1):
            draw_location[y].append("|")
            for x in range(width):
                draw_location[y].append(" ")
            draw_location[y].append("|")
        for x in range(1, width + 1):
            draw_location[0].insert(1, "-")
            draw_location[10].insert(1, "-")

        current = "*"

        for link in self.links:
            start = self.map[link[0]][:]
            end   = self.map[link[1]][:]
            while not (start[0] == end[0] and start[1] == end[1]):
                #Diagonals
                # if start[0] < end[0] and start[1] < end[1]:
                #     start[0] += 1
                #     start[1] += 1
                #     char = "\\"
                # elif start[0] > end[0] and start[1] > end[1]:
                #     start[0] -= 1
                #     start[1] -= 1
                #     char = "\\"
                # elif start[0] < end[0] and start[1] > end[1]:
                #     start[0] += 1
                #     start[1] -= 1
                #     char = "/"
                # elif start[0] > end[0] and start[1] < end[1]:
                #     start[0] -= 1
                #     start[1] += 1
                #     char = "/"
                if start[0] > end[0]:
                    start[0] -= 1
                    char = "."
                elif start[0] < end[0]:
                    start[0] += 1
                    char = "."
                elif start[1] > end[1]:
                    start[1] -= 1
                    char = ":"
                elif start[1] < end[1]:
                    start[1] += 1
                    char = ":"
                else:
                    char = "+"

                if not (start[0] == end[0] and start[1] == end[1]):
                    draw_location[start[1]][start[0]] = char

        for point in self.map:
            if self.location_map[self.map.index(point)] == self.name:
                draw_location[point[1]][point[0]] = current
            else:
                draw_location[point[1]][point[0]] = str(self.map.index(point))

        offset = 1

        self.window.move(1, offset)
        self.window.addstr("You are here: {0}".format(current))
        self.window.move(2, offset)
        for line in draw_location:
            self.window.move(self.window.getyx()[0] + 1, offset)
            for ch in line:
                self.window.addch(ch)
        self.window.move(self.window.getmaxyx()[0] - 2, offset)
        for location in self.location_map:
            if location == self.name:
                self.window.addstr(current + ":" + location + " ")
            else:
                self.window.addstr(str(self.location_map.index(location)) + ":" + location + " ")
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.attroff(curses.color_pair(255))