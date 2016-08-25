from bin.game_objects.stations.station import Station

class Spinningwheel(Station):
    def __init__(self, number, area, name, description):
        super(Spinningwheel, self).__init__(number, area, name, description)
        self.display_name = "spinning wheel"

        self.xp_bounty = {"cotton_fabric" : 30,
                          "flax_linen" : 41,
                          "jute_thread" : 52,
                          "hemp_cloth" : 63,
                          "blood_fabric" : 74,
                          "smoke_slink" : 85}

    def spin(self, fibers):
        cloths = []
        spun_fibers = []
        self.status.start_sequence()
        self.status.output("You begin spinning the fibers into fabric")
        for recipe in self.player.recipes.known_spinningwheel_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_cloths = fibers[:]
                        fiber = None
                        for item in components:
                            potential_cloths.remove(item)
                            fiber = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.time.tick(1)
                        self.status.output("You spin a {0} into {1}".format(fiber, recipe.keys()[0].replace("_", " ")))
                        self.player.gain_xp("alchemy", self.xp_bounty[recipe.keys()[0]])
                        cloths.append(recipe.keys()[0])
                        fibers = potential_cloths
                        spun_fibers.append(components)
            except ValueError:
                pass
        spun_fibers_list = []
        for components in spun_fibers:
            for fiber in components:
                spun_fibers_list.append(fiber)
        self.time.sleep(1)
        self.status.output("You finish spinning fibers")
        self.status.end_sequence()
        return (cloths, spun_fibers_list)