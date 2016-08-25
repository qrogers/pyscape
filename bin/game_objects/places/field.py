from bin.game_objects.places.place import Place

class Field(Place):
    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Field, self).__init__(number, area, name, description, difficulty, level, info)
        #Fiber that can be picked here
        self.fiber = info['fiber']
        #Amount of fiber you can pick per run
        self.gain = info['gain']
        #Amount that is available
        self.amount = info['amount']

        self.time.register_move_event(self.move)

        self.xp_bounty = {"cotton_boll"     : 20,
                          "flax_fiber"      : 30,
                          "jute_fiber"      : 40,
                          "hemp_fiber"      : 50,
                          "crimson_strands" : 60,
                          "shadow_threads"  : 60}

    def forage(self, level):
        if level >= self.level:
            self.status.start_sequence()
            self.status.output("You begin foraging for plant fibers")
            self.time.tick(1)
            self.time.sleep(3)
            gained = self.gain
            if gained > self.amount:
                gained = self.amount
            for x in range(gained):
                self.status.output("You pick a {0}".format(self.fiber.replace("_", " ")))
                self.player.gain_xp("farming", self.xp_bounty[self.fiber])
                self.time.sleep(1)
                self.time.tick(1)
            self.time.sleep(1)
            self.status.output("You have picked all the fibers you can for now, come back later")
            self.status.end_sequence()
            self.amount -= gained
            return (self.fiber, gained)
        else:
            return 1


    def move(self):
        if self.amount < 40:
            self.amount += 5
        else:
            self.amount = 40