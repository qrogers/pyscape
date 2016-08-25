from bin.game_objects.stations.station import Station

class Pestle(Station):
    def __init__(self, number, area, name, description):
        super(Pestle, self).__init__(number, area, name, description)

        self.xp_bounty = {"basil_powder"  : 10,
                          "flower_mix"    : 18,
                          "petal_dust"    : 27,
                          "herbal_salve"  : 36,
                          "fire_essence"  : 45,
                          "black_grounds" : 54}

    def grind(self, plants):
        ingredients = []
        ground_plants = []
        self.status.start_sequence()
        self.status.output("You begin grinding plants")
        for recipe in self.player.recipes.known_pestle_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_plants = plants[:]
                        ingredient = None
                        for item in components:
                            potential_plants.remove(item)
                            ingredient = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.player.gain_xp("alchemy", self.xp_bounty[recipe.keys()[0]])
                        self.time.tick(1)
                        self.status.output("You grind a {0} into a {1}".format(ingredient, recipe.keys()[0].replace("_", " ")))
                        ingredients.append(recipe.keys()[0])
                        plants = potential_plants
                        ground_plants.append(components)
            except ValueError:
                pass
        ground_plants_list = []
        for components in ground_plants:
            for plant in components:
                ground_plants_list.append(plant)
        self.time.sleep(1)
        self.status.output("You finish grinding plants")
        self.status.end_sequence()
        return (ingredients, ground_plants_list)