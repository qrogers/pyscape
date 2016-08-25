from bin.game_objects.places.place import Place
from math import ceil
from random import randint

class Mine(Place):

    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Mine, self).__init__(number, area, name, description, difficulty, level, info)
        #Resources obtainable from the mine
        self.amount = info['amount']
        #Maximum number of ores the mine can have
        self.max_amount = info['max_amount']
        #Maximum number of ores obtainable per run
        self.max_per_run = info['max_per_run']
        #List of ores names obtainable from the mine
        self.ores = info['ores']
        #Amount of ores regenerated by the mine per area move
        self.rate = info['rate']

        self.xp_bounty = {"copper_ore"  : 35,
                          "iron_ore"    : 50,
                          "mithrin_ore" : 65,
                          "adamite_ore" : 80,
                          "demnite_ore" : 95,
                          "nighite_ore" : 110,
                          "spark_ore"   : 110}

        self.time.register_move_event(self.move)

    def mine(self, level):
        if level >= self.level:
            if self.amount <= 0:
                return 2
            total_ores = ((level / (2 * self.difficulty + 0.0)) * self.max_per_run) + randint(0, 2)
            if total_ores > self.max_per_run:
                total_ores = self.max_per_run
            if total_ores > self.amount:
                total_ores = self.amount
            if total_ores <= 0:
                total_ores = 1

            rates = [[1.00],
                     [.60, .40],
                     [.50, .30, .20],
                     [.50, .25, .15, .10],
                     [.50, .25, .13, .7, .5]]

            gain = {}
            i = 0
            for ore in self.ores:
               gain[ore] = int(ceil(total_ores * rates[len(self.ores) - 1][i]))
               i += 1

            self.status.start_sequence()
            self.status.output("You enter the mine")
            self.time.sleep(1)
            for ore in gain:
                self.time.sleep(1)
                self.status.output("You mine {0} {1}".format(gain[ore], ore.replace("_", " ")))
                self.player.gain_xp("gathering", self.xp_bounty[ore] * gain[ore])
                self.amount -= gain[ore]
                self.time.tick(gain[ore])
            self.time.sleep(1)
            self.status.output("You return to the surface")
            self.status.end_sequence()

            return gain
        else:
            return 1

    def prospect(self):
        return str(self.amount) + "/" + str(self.max_amount) + " mpr: " + str(self.max_per_run) + " ores: " + str(self.ores)

    def move(self):
        self.amount += self.rate
        if self.amount > self.max_amount:
            self.amount = self.max_amount