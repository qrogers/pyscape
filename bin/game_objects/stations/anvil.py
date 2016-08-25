from bin.game_objects.stations.station import Station

class Anvil(Station):
    def __init__(self, number, area, name, description):
        super(Anvil, self).__init__(number, area, name, description)

        self.xp_bounty = {"leather_gloves" : 50,
                          "bronze_cape" : 75,
                          "bronze_legs" : 83,
                          "leather_boots" : 78,
                          "bronze_helmet" : 80,
                          "leather_shield" : 63,
                          "bronze_chest" : 100,
                          "bronze_spear" : 90
                          }

    def smith(self, materials, name):
        item_name = None

        item_recipe = None
        for recipe in self.player.recipes.known_anvil_recipes:
            if recipe.keys()[0] == name:
                item_name = name
                item_recipe = recipe

        if item_name is None:
            #Recipe not found
            return 1

        smithed_materials_list = item_recipe[item_name]
        try:
            for material in item_recipe[item_name]:
                materials.remove(material)
        except ValueError:
            #Insufficient materials
            return 2
        self.status.start_sequence()
        self.status.output("You begin creating a {0}".format(item_name.replace("_", " ")))
        self.time.sleep(len(item_recipe[item_name]))
        self.time.tick(len(item_recipe[item_name]))
        self.status.output("You complete the creation of a {0}".format(item_name.replace("_", " ")))
        self.player.gain_xp("crafting", self.xp_bounty[item_name])
        self.status.end_sequence()
        return (item_name, smithed_materials_list)

    def list_makeable_recipes(self, materials):
        options = []
        for recipe in self.player.recipes.known_anvil_recipes:
            try:
                for components in recipe.values():
                    potential_materials = materials[:]
                    for item in components:
                        potential_materials.remove(item)
                    options.append(recipe)
            except ValueError:
                pass

        self.status.start_sequence()
        self.status.output("From your inventory, you can make:")
        items = []
        if options == []:
            self.status.output("Nothing")
        else:
            for recipe in options:
                items.append(recipe.keys()[0])
                materials_string = ""
                for material in recipe.values()[0]:
                    materials_string += material.replace("_", " ") + ", "
                self.status.output("{0} out of {1}".format(recipe.keys()[0].replace("_", " "), materials_string[:len(materials_string) - 2]))
        self.status.end_sequence()
        return items