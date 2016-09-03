import curses
import yaml

class Player():

    def __init__(self, window, var_handler):
        # 12% growth base 100
        self.xp_table = [0, 0, 112, 237, 377, 533, 707, 901, 1118, 1361, 1633, 1937, 2277, 2657, 3082, 3558, 4091, 4687,
                          5354, 6101, 6937, 7873, 8921, 10094, 11407, 12877, 14523, 16366, 18430, 20741, 23329, 26227,
                          29472, 33106, 37176, 41734, 46838, 52554, 58955, 66124, 74153, 83145, 93216, 104495, 117127,
                          131274, 147118, 164863, 184737, 206995, 231923, 000]


        self.xp_to_next = [0, 0, 112, 125, 140, 156, 174, 194, 217, 243, 272, 304, 340, 380, 425, 476, 533, 596, 667,
                           747, 836, 936, 1048, 1173, 1313, 1470, 1646, 1843, 2064, 2311, 2588, 2898, 3245, 3634, 4070,
                           4558, 5104, 5716, 6401, 7169, 8029, 8992, 10071, 11279, 12632, 14147, 15844, 17745, 19874,
                           22258, 24928]

        self.var_handler = var_handler

        self.window = window

        self.status_handler = var_handler.get('status_handler')

        self.area = None
        self.location = None

        self.recipes = self.Recipes()

        self.gathering_level = 1
        self.gathering_current = self.gathering_level
        self.gathering_xp = self.xp_table[self.gathering_level]

        self.crafting_level = 1
        self.crafting_current = self.crafting_level
        self.crafting_xp = self.xp_table[self.crafting_level]
        for x in range(1, self.crafting_level + 1):
            self.learn_recipe("crafting", x)

        self.hunting_level = 1
        self.hunting_current = self.hunting_level
        self.hunting_xp = self.xp_table[self.hunting_level]

        self.alchemy_level = 1
        self.alchemy_current = self.alchemy_level
        self.alchemy_xp = self.xp_table[self.alchemy_level]
        for x in range(1, self.alchemy_level + 1):
            self.learn_recipe("alchemy", x)

        self.farming_level = 1
        self.farming_current = self.farming_level
        self.farming_xp = self.xp_table[self.farming_level]

        self.stealth_level = 1
        self.stealth_current = self.stealth_level
        self.stealth_xp = self.xp_table[self.stealth_level]

        self.health_level = 5
        self.health_current = 5
        self.health_xp = self.xp_table[self.health_level]

        self.attack_level = 1
        self.attack_current = self.attack_level
        self.attack_xp = self.xp_table[self.attack_level]

        self.defense_level = 1
        self.defense_current = self.defense_level
        self.defense_xp = self.xp_table[self.defense_level]

        self.proficiency_level = 1
        self.proficiency_current = self.proficiency_level
        self.proficiency_xp = self.xp_table[self.proficiency_level]

        self.magic_level = 1
        self.magic_current = self.magic_level
        self.magic_xp = self.xp_table[self.magic_level]
        for x in range(1, self.magic_level + 1):
            self.learn_recipe("magic", x)

        self.buffs = []

        self.update_skill_window()

    def die(self):
        raise NotImplementedError("Not implemented: player.die")

    def add_buff(self, buff):
        self.buffs.append(buff)
        buff.apply()
        self.update_skill_window()

    def remove_buff(self, buff):
        self.buffs.remove(buff)
        buff.remove()
        self.update_skill_window()

    def buff_skill(self, skill, amount):
        setattr(self, skill + "_current", getattr(self, skill + "_current") + amount)

    def take_damage(self, damage):
        self.health_current -= damage
        self.update_skill_window()
        if self.health_current <= 0:
            self.die()
            return "dead"
        return "alive"

    def gain_xp(self, skill, amount):
        skill_xp = getattr(self, skill + "_xp") + amount
        setattr(self, skill + "_xp", skill_xp)
        skill_level = getattr(self, skill + "_level")
        while skill_level < 50 and skill_xp >= self.xp_table[skill_level + 1]:
            self.level_up(skill)
            skill_level = getattr(self, skill + "_level")

        self.update_skill_window()
        self.var_handler.get('spell_handler').update_window()

    def level_up(self, skill):
        skill_level = getattr(self, skill + "_level")
        skill_level += 1
        setattr(self, skill + "_level", skill_level)
        setattr(self, skill + "_current", getattr(self, skill + "_current") + 1)
        recipes = self.learn_recipe(skill, skill_level)
        recipes_str = "You can now make:\n"
        for recipe in recipes:
            recipes_str += recipe.keys()[0] + ", "
        self.status_handler.output("{0} level up! {1}".format((skill[:1].upper() + skill[1:]), skill_level), curses.color_pair(1))
        if recipes != []:
            self.status_handler.output(recipes_str.strip(", "))

    def learn_recipe(self, skill, level):
        recipes = []
        if skill == "crafting":
            for object in self.recipes.all_crafting_recipes:
                if level in self.recipes.all_crafting_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_crafting_recipes[object][level]:
                        recipe_list.append(recipe)
                        recipes.append(recipe)
        elif skill == "alchemy":
            for object in self.recipes.all_alchemy_recipes:
                if level in self.recipes.all_alchemy_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_alchemy_recipes[object][level]:
                        recipe_list.append(recipe)
                        recipes.append(recipe)
        elif skill == "magic":
            for object in self.recipes.all_magic_recipes:
                if level in self.recipes.all_magic_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_magic_recipes[object][level]:
                        recipe_list.append(recipe)
                        recipes.append(recipe)
        return recipes

    def forget_recipe(self, skill, level):
        if skill == "crafting":
            for object in self.recipes.all_crafting_recipes:
                if level in self.recipes.all_crafting_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_crafting_recipes[object][level]:
                        recipe_list.remove(recipe)
        elif skill == "alchemy":
            for object in self.recipes.all_alchemy_recipes:
                if level in self.recipes.all_alchemy_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_alchemy_recipes[object][level]:
                        recipe_list.remove(recipe)
        elif skill == "magic":
            for object in self.recipes.all_magic_recipes:
                if level in self.recipes.all_magic_recipes[object].keys():
                    recipe_list = getattr(self.recipes, "known_" + object + "_recipes")
                    for recipe in self.recipes.all_magic_recipes[object][level]:
                        recipe_list.remove(recipe)

    def set_level(self, skill, level):
        current = getattr(self, skill + "_level")
        setattr(self, skill + "_level", level)
        setattr(self, skill + "_current", getattr(self, skill + "_current") + level - current)
        if current < getattr(self, skill + "_level"):
            for x in range(current, getattr(self, skill + "_level") + 1):
                self.learn_recipe(skill, x)
        elif current > getattr(self, skill + "_level"):
            for x in range(getattr(self, skill + "_level"), current + 1):
                self.forget_recipe(skill, x)

        self.update_skill_window()
        self.var_handler.get('spell_handler').update_window()

    def move_area(self, area):
        self.area = area
        self.location = area.location

    def get_status(self):
        return "Health: {0}/{1}".format(self.health_current, self.health_level)

    def update_skill_window(self):
        #TODO: Show xp gains
        self.window.attron(curses.color_pair(254))
        self.window.erase()
        self.window.move(1, 1)
        self.window.addstr("Gathering:   {0}/{1} XP: {2}/{3}".format(self.gathering_current, self.gathering_level,
                                                                    self.gathering_xp,
                                                                    self.xp_table[self.gathering_level + 1]))
                                                                    #self.xp_table[self.gathering_level + 1] - self.gathering_xp))
        self.window.move(2, 1)
        self.window.addstr("Crafting:    {0}/{1} XP: {2}/{3}".format(self.crafting_current, self.crafting_level,
                                                                    self.crafting_xp,
                                                                    self.xp_table[self.crafting_level + 1]))
        self.window.move(3, 1)
        self.window.addstr("Hunting:     {0}/{1} XP: {2}/{3}".format(self.hunting_current, self.hunting_level,
                                                                    self.hunting_xp,
                                                                    self.xp_table[self.hunting_level + 1]))
        self.window.move(4, 1)
        self.window.addstr("Alchemy:     {0}/{1} XP: {2}/{3}".format(self.alchemy_current, self.alchemy_level,
                                                                    self.alchemy_xp,
                                                                    self.xp_table[self.alchemy_level + 1]))
        self.window.move(5, 1)
        self.window.addstr("Farming:     {0}/{1} XP: {2}/{3}".format(self.farming_current, self.farming_level,
                                                                    self.farming_xp,
                                                                    self.xp_table[self.farming_level + 1]))
        self.window.move(7, 1)
        self.window.addstr("Stealth:     {0}/{1} XP: {2}/{3}".format(self.stealth_current, self.stealth_level,
                                                                    self.stealth_xp,
                                                                    self.xp_table[self.stealth_level + 1]))
        self.window.move(8, 1)
        self.window.addstr("Health:      {0}/{1} XP: {2}/{3}".format(self.health_current, self.health_level,
                                                                    self.health_xp,
                                                                    self.xp_table[self.health_level + 1]))
        self.window.move(9, 1)
        self.window.addstr("Attack:      {0}/{1} XP: {2}/{3}".format(self.attack_current, self.attack_level,
                                                                    self.attack_xp,
                                                                    self.xp_table[self.attack_level + 1]))
        self.window.move(10, 1)
        self.window.addstr("Defense:     {0}/{1} XP: {2}/{3}".format(self.defense_current, self.defense_level,
                                                                    self.defense_xp,
                                                                    self.xp_table[self.defense_level + 1]))
        self.window.move(11, 1)
        self.window.addstr("Proficiency: {0}/{1} XP: {2}/{3}".format(self.proficiency_current, self.proficiency_level,
                                                                    self.proficiency_xp,
                                                                    self.xp_table[self.proficiency_level + 1]))
        self.window.move(12, 1)
        self.window.addstr("Magic:       {0}/{1} XP: {2}/{3}".format(self.magic_current, self.magic_level,
                                                                    self.magic_xp,
                                                                    self.xp_table[self.magic_level + 1]))
        self.window.attron(curses.color_pair(255))
        self.window.box()
        self.window.refresh()

    class Recipes():
        def __init__(self):
            self.known_sawmill_recipes       = []
            self.known_furnace_recipes       = []
            self.known_anvil_recipes         = []
            self.known_tannery_recipes       = []

            self.known_stove_recipes         = []
            self.known_pestle_recipes        = []
            self.known_spinningwheel_recipes = []
            self.known_cauldron_recipes      = []

            self.known_focus_recipes         = []

            all_recipes = yaml.load(open("conf/recipes.yaml"))
            self.all_crafting_recipes = all_recipes['all_crafting_recipes']
            self.all_alchemy_recipes  = all_recipes['all_alchemy_recipes']
            self.all_magic_recipes    = all_recipes['all_magic_recipes']