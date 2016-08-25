from bin.game_objects.stations.station import Station

class Tannery(Station):
    def __init__(self,  number, area, name, description):
        super(Tannery, self).__init__( number, area, name, description)

        self.xp_bounty = {"deer_leather": 47,
                          "lizard_leather": 57,
                          "tiger_leather" : 67,
                          "wyvern_leather" : 77,
                          "demon_leather" : 87,
                          "dragon_leather" : 97,
                          "black_leather" : 97}

    def tan(self, hides):
        leathers = []
        tanned_hides = []
        self.status.start_sequence()
        self.status.output("You begin tanning the hides into leather")
        for recipe in self.player.recipes.known_tannery_recipes:
            try:
                #Until the recipe cannot be created and raises a value error
                while True:
                    for components in recipe.values():
                        potential_leathers = hides[:]
                        hide = None
                        for item in components:
                            potential_leathers.remove(item)
                            hide = item.replace("_", " ")
                        self.time.sleep(len(components))
                        self.time.tick(1)
                        self.status.output("You tan a {0} into a {1}".format(hide, recipe.keys()[0].replace("_", " ")))
                        self.player.gain_xp("crafting", self.xp_bounty[recipe.keys()[0]])
                        leathers.append(recipe.keys()[0])
                        hides = potential_leathers
                        tanned_hides.append(components)
            except ValueError:
                pass
        tanned_hides_list = []
        for components in tanned_hides:
            for hide in components:
                tanned_hides_list.append(hide)
        self.time.sleep(1)
        self.status.output("You finish tanning hides")
        self.status.end_sequence()
        return (leathers, tanned_hides_list)