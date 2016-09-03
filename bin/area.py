from unit_handler import UnitHandler
import game_objects.npcs as npcs
import game_objects.places as places
import game_objects.stations as stations

class Area():

    #TODO: Add rift spawning
    #TODO: Set spawning when inactive

    def __init__(self, name, location, conf, var_handler):
        self.name = name
        self.display_name = (name[:1].upper() + name[1:]).replace("_", " ")
        self.location = location
        self._conf = conf
        self.var_handler = var_handler
        self.description = self._conf['description']
        self.text = self._conf['text']
        self.triggers = self._conf['triggers']
        self.game_objects = dict()
        self.game_objects['units'] = []
        self.game_objects['npcs'] = []
        self.game_objects['places'] = []
        self.game_objects['stations'] = []

        self.base_threat = self._conf['base_threat']
        self.risk = self._conf['risk']
        self.recovery = self._conf['recovery']
        self.threat = self.base_threat
        self.max_enemies = self._conf['max_enemies']

        self.active = False

        self.unit_handler = UnitHandler(self, var_handler)

        for unit in self._conf['game_objects']['units']:
            self.unit_handler.add_spawner(unit[0], unit[1])

        for npc in self._conf['game_objects']['npcs']:
            self.spawn_game_object(self._conf['game_objects']['npcs'][npc], 'npcs', npc)

        for place in self._conf['game_objects']['places']:
            self.spawn_game_object(self._conf['game_objects']['places'][place], 'places', place)

        for station in self._conf['game_objects']['stations']:
            self.spawn_game_object(self._conf['game_objects']['stations'][station], 'stations', station)

    def spawn_game_object(self, info, object_type, name):
        new_object = None
        if object_type == 'npcs':
            new_object = getattr(getattr(npcs, name), name[:1].upper() + name[1:])(len(self.game_objects['npcs']),
                                                        self, name, info['description'], info)
        elif object_type == 'places':
            new_object = getattr(getattr(places, name), name[:1].upper() + name[1:])(len(self.game_objects['places']),
                                                        self, name, info['description'], info['difficulty'],
                                                        info['level'], info)
        elif object_type == 'stations':
            new_object = getattr(getattr(stations, name), name[:1].upper() + name[1:])(len(self.game_objects['stations']
                                                                                           ), self, name, info['description'])
        self.game_objects[object_type].append(new_object)
        return new_object

    def remove_game_object(self, object, object_type):
        self.game_objects[object_type].remove(object)

    def get_object(self, category, type):
        for object in self.game_objects[category]:
            if object.class_name == type:
                return object

    def activate(self):
        self.active = True
        self.unit_handler.activate()
        self.run_triggers("arrive")

    def deactivate(self):
        self.active = False
        self.unit_handler.deactivate()
        self.run_triggers("leave")
        self.var_handler.get('time_handler').deregister_tick_event(self.tick)

    def run_triggers(self, action):
        def validate(condition, trigger):

            def first(trigger):
                return True

            def inventory_contains(trigger):
                return self.var_handler.get('inventory_handler').in_inventory(trigger[0]) is not None

            conditions = {"first" : first, "inventory_contains" : inventory_contains}

            return conditions[condition](trigger)

        self.var_handler.get('time_handler').register_tick_event(self.tick)
        self.var_handler.get('status_handler').start_sequence()
        if action in self.triggers.keys():
            for condition in self.triggers[action].keys():
                    for trigger in self.triggers[action][condition]:
                        if validate(condition, trigger):
                            if trigger[1] == "text":
                                for line in self.text[action][condition][trigger[0]]:
                                    self.var_handler.get('status_handler').slow_output(line, self.var_handler.get('time_handler'))
                            trigger[2] -= 1
                            if trigger[2] == 0:
                                del self.triggers[action][condition]
        self.var_handler.get('status_handler').end_sequence()

    def tick(self):
       self.threat += self.risk
       attacker = self.unit_handler.tick(self.threat)
       if attacker is not None:
           self.var_handler.get('combat_handler').start_combat(attacker)
