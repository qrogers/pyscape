from bin.game_objects.stations.station import Station

class Furnace(Station):
    def __init__(self, number, area, name, description):
        super(Furnace, self).__init__(number, area, name, description)

        self.xp_bounty = {"bronze_bar"  : 10,
                          "steel_bar"   : 20,
                          "mithril_bar" : 30,
                          "adamant_bar" : 40,
                          "dread_bar"   : 50,
                          "infused_bar" : 60,
                          "shadow_bar"  : 60}

    def smelt(self, ores):
        bars = []
        smelted_ores = []
        #recipe = {result : [1, 2, 3]}
        #components = [1, 2, 3]
        #item = 1
        self.status.start_sequence()
        self.status.output("You begin smelting ores into bars")
        for recipe in self.player.recipes.known_furnace_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_ores = ores[:]
                        ore = None
                        for item in components:
                            potential_ores.remove(item)
                            ore = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.time.tick(1)
                        self.status.output("You smelt {0} {1} into a {2}".format(len(components), ore, recipe.keys()[0].replace("_", " ")))
                        self.player.gain_xp("crafting", self.xp_bounty[recipe.keys()[0]])
                        bars.append(recipe.keys()[0])
                        ores = potential_ores
                        smelted_ores.append(components)
            except ValueError:
                pass
        smelted_ores_list = []
        for components in smelted_ores:
            for ore in components:
                smelted_ores_list.append(ore)
        self.time.sleep(1)
        self.status.output("You finish smelting")
        self.status.end_sequence()
        return (bars, smelted_ores_list)