import game_objects.units as units
from random import randint

#TODO: Spawn units over time

class UnitHandler():

    def __init__(self, area, var_handler):
        self.area = area
        self.units = self.area.game_objects['units']
        self.var_handler = var_handler
        self.spawners = []

    def spawn_unit(self, name):
        class_name = name[:1].upper() + name[1:]
        try:
            new_unit = getattr(getattr(units, name), class_name)(len(self.units), self.area, name)
        except AttributeError as e:
            raise e
            #should give error for unit not found
        new_unit.die = self.kill
        self.area.game_objects['units'].append(new_unit)

    def add_spawner(self, unit, interval):
        self.spawners.append(self.Spawner(unit, self, interval, self.var_handler.get('time_handler'), self.spawn_unit))

    def tick(self, threat):
        for unit in self.units:
            chance = int(((threat + unit.aggression) / 10) - self.var_handler.get('player').stealth_current)
            if randint(0, 100) <= chance:
                return unit
        return None

    def activate(self):
        for spawner in self.spawners:
            spawner.activate()

    def deactivate(self):
        for spawner in self.spawners:
            spawner.deactivate()

        #Based on current threat, player stealth and unit aggression, chance for unit to attack
        #(threat + aggression) - stealth / 10 = %
        #baseline:    0 threat 0 stealth    0 aggression   0%
        #topline:  1000 threat 0 stealth    0 aggression 100%
        #seekndes:    0 threat 0 stealth 1000 aggression 100%
        #middle:    500 threat 0 stealth  500 aggression  50%

    def kill(self, unit):
        self.area.remove_game_object(unit, 'units')
        drops = unit.drops[:]
        drops.reverse()
        for drop in drops:
            if randint(1, 100) <= drop[0]:
                inventory = self.var_handler.get('inventory_handler')
                item = drop[1].split("-", 1)
                amount = item[0]
                name = item[1]
                if name == "gold":
                    inventory.change_gold(amount)
                else:
                    inventory.add_item("*", "*", name, int(amount))
                self.var_handler.get('status_handler').output("Received drop:{0} {1}".format("" if amount == "1" else " " + amount, name.replace("_", " ")))
                break
        player = self.var_handler.get('player')
        for skill in unit.xp:
            player.gain_xp(skill[0], skill[1])

    def get_units(self):
        return self.units

    def get_unit_by_display_name(self, name):
        for unit in self.units:
            if unit.display_name == name:
                return unit
        return None

    class Spawner():

        def __init__(self, unit, unit_handler, interval, time, spawn):
            self.unit = unit
            self.unit_handler = unit_handler
            self.interval = interval
            self.time = time
            self.count = 0
            self.spawn = spawn

        def activate(self):
            self.time.register_tick_event(self.tick)

        def deactivate(self):
            self.time.deregister_tick_event(self.tick)

        def tick(self):
            self.count += 1
            if self.count >= self.interval:
                self.count = 0
                if len(self.unit_handler.units) < self.unit_handler.area.max_enemies:
                    self.spawn(self.unit)