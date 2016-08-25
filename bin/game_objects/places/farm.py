from bin.game_objects.places.place import Place
from random import randint

class Farm(Place):
    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Farm, self).__init__(number, area, name, description, difficulty, level, info)
        #Base time factor for growing
        self.duration = info['duration']
        #Base number of plants grown
        self.size = info['size']
        #Random range added to gain
        self.variance = info['variance']
        #What plants can be grown in this farm
        self.plants = info['plants']

        self.plant_levels = {"basil" : 1,
                             "lily" : 10,
                             "orchid" : 20,
                             "rhysiro" : 30,
                             "firelid" : 40,
                             "shaliss" : 50}

        self.plant_names = {"basil"   : "basil_leaf",
                            "lily"    : "lily_flower",
                            "orchid"  : "orchid_petal",
                            "rhysiro" : "rhysiro_leaf",
                            "firelid" : "firelid_flower",
                            "shaliss" : "shaliss_petal"}

        self.xp_bounty = {"basil" : 20,
                          "lily" : 35,
                          "orchid" : 60,
                          "rhysiro" : 95,
                          "firelid" : 140,
                          "shaliss" : 195}

        self.crop = None
        self.time_to_grow = 0

    def farm(self, level, plant):
        self.status.start_sequence()
        if self.crop is None:
            if plant in self.plant_levels.keys():
                if plant in self.plants:
                    if level >= self.plant_levels[plant]:
                        self.status.output("You begin planting {0} seeds".format(plant))
                        self.time.sleep(5)
                        self.time.tick(5)
                        self.crop = plant
                        grow_time = self.difficulty + (self.plant_levels[plant] / 2) + randint(-4, 2) - (level * 1.25)
                        grow_time *= .4
                        if grow_time < 1:
                            grow_time = 1
                        grow_time *= self.duration
                        self.time_to_grow = int(grow_time)
                        self.player.gain_xp("farming", 4)
                        self.time.sleep(2)
                        self.time.tick(1)
                        self.time.register_tick_event(self.tick)
                        self.time.register_move_event(self.move)
                        self.status.output("You finish planting {0} seeds".format(plant))
                        self.status.output("They will take {0} ticks to grow".format(grow_time))
                        self.status.end_sequence()
                        #Crop planted
                        return 4
                    else:
                        self.status.end_sequence()
                        #Level too low
                        return 3
                else:
                    self.status.end_sequence()
                    #Plant cant be grown here
                    return 6
            else:
                self.status.end_sequence()
                if plant == "":
                    #No plant given
                    return 5
                #Unknown plant
                return 2
        elif self.time_to_grow <= 0:
            self.time.deregister_tick_event(self.tick)
            self.time.deregister_move_event(self.move)
            crop = self.crop
            self.crop = None
            amount = self.size + randint(self.variance * -1, self.variance)
            self.status.output("You begin harvesting the grown {0}".format(crop))
            self.time.sleep(amount)
            self.time.tick(amount)
            self.player.gain_xp("farming", amount * self.xp_bounty[crop])
            self.status.output("You fishing harvesting")
            self.status.end_sequence()
            return (self.plant_names[crop], amount)

        else:
            #Still growing
            self.status.end_sequence()
            return 1

    def tick(self):
        if self.time_to_grow > 0:
            self.time_to_grow -= 1

    def move(self):
        if self.time_to_grow > 0:
            self.time_to_grow -= 3