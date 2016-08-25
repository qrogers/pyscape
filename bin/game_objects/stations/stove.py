from bin.game_objects.stations.station import Station

class Stove(Station):
    def __init__(self, number, area, name, description):
        super(Stove, self).__init__(number, area, name, description)

        self.xp_bounty = {"cooked_venison" : 30,
                          "cooked_lizard" : 45,
                          "cooked_tiger" : 60,
                          "cooked_wyvion" : 75,
                          "cooked_demnage" : 90,
                          "cooked_dragon" : 105,
                          "cooked_nighton" : 105}

    def cook(self, meats):
        foods = []
        cooked_meats = []
        self.status.start_sequence()
        self.status.output("You begin cooking the raw meat")
        for recipe in self.player.recipes.known_stove_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_foods = meats[:]
                        food = None
                        for item in components:
                            potential_foods.remove(item)
                            food = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.time.tick(1)
                        self.status.output("You cook {0}".format(food, recipe.keys()[0].replace("_", " ")))
                        self.player.gain_xp("alchemy", self.xp_bounty[recipe.keys()[0]])
                        foods.append(recipe.keys()[0])
                        meats = potential_foods
                        cooked_meats.append(components)
            except ValueError:
                pass
        cooked_meats_list = []
        for components in cooked_meats:
            for food in components:
                cooked_meats_list.append(food)
        self.time.sleep(1)
        self.status.output("You finish cooking")
        self.status.end_sequence()
        return (foods, cooked_meats_list)