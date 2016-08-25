from location import Location
import yaml

class LocationHandler():

    def __init__(self, window, var_handler):
        self.conf_dir = "conf/game_objects/locations/"
        self.var_handler = var_handler
        self.window = window
        self.locations = {}

    def spawn_location(self, name):
        if name not in self.locations.keys():
            conf = yaml.load(open(self.conf_dir + name + "/" + name + ".yaml"))
            new_location = Location(name, conf, self.window, self.var_handler)
            self.locations[name] = new_location
            return new_location
        else:
            raise NameError("location: " + name + " already exists")


    def get_location(self, location):
        return self.locations[location]