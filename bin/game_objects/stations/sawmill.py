from bin.game_objects.stations.station import Station

class Sawmill(Station):
    def __init__(self, number, area, name, description):
        super(Sawmill, self).__init__(number, area, name, description)

        self.xp_bounty = {"oak_plank"    : 10,
                          "maple_plank"  : 20,
                          "willow_plank" : 30,
                          "alder_plank"  : 40,
                          "elder_plank"  : 50,
                          "imbued_plank" : 60,
                          "ebony_plank"  : 60}

    def mill(self, logs):
        planks = []
        cut_logs = []
        self.status.start_sequence()
        self.status.output("You begin milling the logs into planks")
        for recipe in self.player.recipes.known_sawmill_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_logs = logs[:]
                        plank = None
                        for item in components:
                            potential_logs.remove(item)
                            plank = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.player.gain_xp("crafting", self.xp_bounty[recipe.keys()[0]])
                        self.time.tick(1)
                        self.status.output("You mill a {0} into a {1}".format(plank, recipe.keys()[0].replace("_", " ")))
                        planks.append(recipe.keys()[0])
                        logs = potential_logs
                        cut_logs.append(components)
            except ValueError:
                pass
        cut_logs_list = []
        for components in cut_logs:
            for log in components:
                cut_logs_list.append(log)
        self.time.sleep(1)
        self.status.output("You finish milling logs")
        self.status.end_sequence()
        return (planks, cut_logs_list)