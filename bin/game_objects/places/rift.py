from bin.game_objects.places.place import Place

class Rift(Place):
    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Rift, self).__init__(number, area, name, description, difficulty, level, info)
        #The type of energy in this rift
        self.energy = info['energy']
        #The amount of energy harvested from the rift
        self.amount = info['amount']

        self.xp_bounty = {"mystic_energy"  : 20,
                          "cosmic_energy"  : 40,
                          "raging_energy"  : 65,
                          "psionic_energy" : 95,
                          "demonic_energy" : 130,
                          "spark_energy"   : 170,
                          "dark_energy"    : 170}

    def harness(self, level):
        if level >= self.level:
            self.status.start_sequence()
            self.status.output("You begin harnessing {0} energy from the rift".format(self.energy))
            self.time.sleep(1)
            for x in range(self.amount):
                self.status.output("You begin harness a fragment of {0} energy".format(self.energy))
                self.time.sleep(self.difficulty)
            self.player.gain_xp("magic", self.xp_bounty[self.energy] * self.amount)
            self.status.output("You have harnessed all the energy you can from the rift and it collapses into nothingness")
            self.status.start_sequence()
            return (self.energy, self.amount)
        else:
            return 1