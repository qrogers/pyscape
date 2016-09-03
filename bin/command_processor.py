import curses
import yaml

DEBUG = True

class CommandProcessor():
    #TODO: Add unequip
    #TODO: Add analyze for all places/finish prospect
    #TODO: Add creating new aliases
    #TODO: Add list dropped items command (take with no args)
    #TODO: Add shop commands

    def __init__(self, var_handler):
        self.command_actions = CommandActions(var_handler)

        self.command_dictionary = {}

        command_info = yaml.load(open("conf/commands/commands.yaml"))

        for command in command_info:
            command_prams = command_info[command]
            if "debug" not in command_prams.keys() or DEBUG:
                self.command_dictionary[command] = Command(command, command_prams['num_args'], command_prams['usage'],
                                                           command_prams['info'], command_prams['color'],
                                                           getattr(self.command_actions, command + "_command"))

        self.var_handler = var_handler

        self.aliases = {"plant" : "farm", "pestle" : "grind", "field" : "forage", "track" : "hunt",
                        "pick" : "farm", "chop" : "cut", "man" : "info", "make" : "smith", "grow" : "farm",
                        "mix" : "brew", "gather" : "forage"}

    def receive_command(self, cmd):
        command = cmd.split(' ')[0]
        args = cmd.split(' ')[1:]
        for arg in args:
            if len(arg.strip()) == 0:
                args.remove(arg)
        return self._validate_command(command, args)

    def _validate_command(self, command, args):
        if command in self.command_dictionary.keys():
            if len(args) in self.command_dictionary[command].num_args:
                return self._execute_command(command, args)
            else:
                return (self.command_dictionary[command].usage, curses.color_pair(0) + curses.A_BOLD)
        else:
            if command in self.aliases.keys():
                try:
                    return self._validate_command(self.aliases[command], args)
                except RuntimeError:
                    return ("That command is part of a loop of aliases\nYou need to change one of the aliases", curses.color_pair(2) + curses.A_UNDERLINE)
            else:
                return ("Invalid command", curses.color_pair(2) + curses.A_UNDERLINE)

    def _execute_command(self, command, args):
        return self.command_dictionary[command].run(args)

class CommandActions():
    def __init__(self, var_handler):
        self.var_handler = var_handler

    def status_command(self, args):
        return self.var_handler.get('player').get_status()

    #DEBUG COMMANDS

    def spawn_command(self, args):
        return self.var_handler.get('player').area.spawn_game_object(args[0], 'units', args[0]).get_name()

    def tick_command(self, args):
        try:
            ticks = int(args[0])
            self.var_handler.get('time_handler').tick(ticks)
            return "Ticked {0}".format(ticks)
        except ValueError as ve:
            return ve.message

    def xp_command(self, args):
        player = self.var_handler.get('player')
        player.gain_xp(args[0], int(args[1]))
        return "You gain {0} {1} xp".format(args[1], args[0])

    def level_command(self, args):
        player = self.var_handler.get('player')
        player.set_level(args[0], int(args[1]))
        return "{0} level set to {1}".format(args[0], args[1])

    def create_command(self, args):
        inventory = self.var_handler.get('inventory_handler')
        if len(args) == 3:
            amount = args[2]
        else:
            amount = 1
        try:
            inventory.add_item("*", "*", args[0] + "_" + args[1], int(amount))
        except ValueError:
            return "That is not an item"
        return "Added {0} {1} to your inventory".format(amount, args[0] + "_" + args[1])

    def gold_command(self, args):
        inventory = self.var_handler.get('inventory_handler')
        inventory.change_gold(args[0])
        return "you gain {0} gold".format(args[0])

    #REGULAR COMMANDS

    def attack_command(self, args):
        for unit in self.var_handler.get('player').area.game_objects['units']:
            if unit.name == args[0]:
                self.var_handler.get('combat_handler').start_combat(unit)
                return "Combat over"
        return "There are no {0} here to attack".format(args[0])

    def cast_command(self, args):
        return self.var_handler.get('spell_handler').cast(args[0])

    def list_command(self, args):
        objects = ""
        object_list = []
        for object_type in self.var_handler.get('player').area.game_objects:
            object_list += self.var_handler.get('player').area.game_objects[object_type]
        if len(args) == 0:
            if len(object_list) > 0:
                for game_object in object_list:
                    objects += game_object.name + " "
                    if len(objects.split("\n")[len(objects.split("\n")) - 1]) > 50:
                        objects += "\n"
                return objects.strip().replace(" ", ", ")
            else:
                objects += "Nothing in this area"
                return objects
        else:
            arg = args[0]
            #Correct non plural args
            if arg[len(arg) - 1] != 's':
                arg += 's'
            try:
                if len(self.var_handler.get('player').area.game_objects[arg]) > 0:
                    for game_object in self.var_handler.get('player').area.game_objects[arg]:
                            objects += game_object.name + " "
                    return objects.strip().replace(" ", ", ")
                else:
                    objects += "No {0} in this area".format(arg)
                    return objects
            except KeyError:
                return "{0} is not a type of thing".format(args[0])

    def examine_command(self, args):
        item_name = str(args).replace('\'', '').replace('[', '').replace(']', '').replace(',', '')
        item = self.var_handler.get('inventory_handler').in_inventory(item_name)
        if item is not None:
            return item.examine
        else:
            return "no {0} found in inventory".format(item_name)

    def store_command(self, args):
        area = self.var_handler.get('player').area
        bank = area.get_object('npcs', 'bank')
        if bank is None:
            return "There is no bank here"
        inventory = self.var_handler.get('inventory_handler')
        if len(args) > 1:
            item_name = args[0] + "_" + args[1]
        elif args[0] == "all":
            item_name = "everything"
        else:
            item_name = args[0]
        store = []
        all = "all" in args or (len(args) == 1 and args[0] == "everything")
        if not all:
            if len(args) == 3:
                amount = int(args[2])
            else:
                amount = 1
        else:
            amount = len(inventory.items)
        if amount == 0:
            return "You can't store nothing"
        for item in inventory.items:
            if amount > 0:
                if item.name == item_name or (all and item_name == "everything"):
                    store.append(item)
                    amount -= 1
            else:
                break
        if len(store) > 0:
            for item in store:
                banked = inventory.store(item)
                if banked == 1:
                    return "Your bank is full"
            return "You store {0}".format(item_name)
        else:
            return "There is no {0} in your inventory".format(item_name)

    def withdraw_command(self, args):
        area = self.var_handler.get('player').area
        bank = area.get_object('npcs', 'bank')
        if bank is None:
            return "There is no bank here"
        inventory = self.var_handler.get('inventory_handler')
        if len(args) > 1:
            item_name = args[0] + "_" + args[1]
        elif args[0] == "all":
            item_name = "everything"
        else:
            item_name = args[0]
        withdraw = []
        all = "all" in args or (len(args) == 1 and args[0] == "everything")
        if not all:
            if len(args) == 3:
                amount = int(args[2])
            else:
                amount = 1
        else:
            amount = len(inventory.bank)
        if amount == 0:
            return "You can't withdraw nothing"
        for item in inventory.bank:
            if amount > 0:
                if item.name == item_name or (all and item_name == "everything"):
                    withdraw.append(item)
                    amount -= 1
            else:
                break
        if len(withdraw) > 0:
            for item in withdraw:
                drawn = inventory.withdraw(item)
                if drawn == 1:
                    return "You withdraw as much as you can"
            return "You withdraw {0}".format(item_name)
        else:
            return "There is no {0} in your inventory".format(item_name)

    def bank_command(self, args):
        inventory = self.var_handler.get('inventory_handler')
        inventory.display = "bank" if inventory.display == "inventory" else "inventory"
        inventory.update_inv_window()
        return ""

    def anvil_command(self, args):
        player = self.var_handler.get('player')
        if len(args) == 0:
            items = ""
            for recipe in player.recipes.known_anvil_recipes:
                items += recipe.keys()[0] + " "
                if len(items.split("\n")[len(items.split("\n")) - 1]) > 50:
                    items += "\n"
            return items.strip().replace(" ", ", ")
        else:
            for recipe in player.recipes.known_anvil_recipes:
                if recipe.keys()[0] == args[0] + "_" + args[1]:
                    recipe_str = "{0} are made from:\n".format(args[0] + " " + args[1])
                    count = {}
                    for material in recipe[args[0] + "_" + args[1]]:
                        count[material] = count.get(material, 0) + 1
                    for material in count.keys():
                        recipe_str += "{0} {1}, ".format(count[material], material)
                    return recipe_str.strip(", ")
            return "You do not know how to make that item at an anvil"

    def info_command(self, args):
        try:
            info = self.var_handler.get('command_processor').command_dictionary[args[0]].info
            return info
        except KeyError:
            if args[0] in self.var_handler.get('command_processor').aliases.keys():
                return "{0} is an alias for {1}, use info {1} for information".format(args[0], self.var_handler.get('command_processor').aliases[args[0]])
            return "{0} is not a valid command".format(args[0])

    def stats_command(self, args):
        inventory = self.var_handler.get('inventory_handler')
        gear_name = args[0] + "_" + args[1]
        gear = None
        for item in inventory.items:
            if item.name == gear_name:
                gear = item
                break
        if gear.category != "gear":
            return "Only worn items have stats"
        stats = {}
        for stat in gear.stats:
            for buff in stat.keys():
                try:
                    stats[buff] += stat[buff]
                except KeyError:
                    stats[buff]  = stat[buff]
        stats_string = ""
        for stat in stats.keys():
            stats_string += (stat[:1].upper() + stat[1:]) + " +" + str(stats[stat]) + " "
        if gear.enchantment is not None:
            stats_string += "Enchantment: " + gear.enchantment.name
        return stats_string

    def take_command(self, args):
        #TODO: take all
        item_name = args[0] + "_" + args[1]
        inventory = self.var_handler.get('inventory_handler')
        take = None
        for item in inventory.dropped:
            if item.name == item_name:
                take = item
                break
        if take is not None:
            taken = inventory.take(take)
            if taken == 1:
                return "You do not have room in your inventory to take that"
            return "You take {0}".format(item_name)
        else:
            return "There is no {0} to take".format(item_name)

    def drop_command(self, args):
        if len(args) > 1:
            item_name = args[0] + "_" + args[1]
        elif args[0] == "all":
            item_name = "everything"
        else:
            item_name = args[0]
        if item_name == "the_bass":
            return "wub wub wub"
        inventory = self.var_handler.get('inventory_handler')
        drop = []
        all = "all" in args or (len(args) == 1 and args[0] == "everything")
        if not all:
            if len(args) == 3:
                amount = int(args[2])
            else:
                amount = 1
        else:
            amount = len(inventory.items)
        if amount == 0:
            return "You can't drop nothing"
        for item in inventory.items:
            if amount > 0:
                if item.name == item_name or (all and item_name == "everything"):
                    drop.append(item)
                    amount -= 1
            else:
                break
        if len(drop) > 0:
            for item in drop:
                inventory.drop(item)
            return "You drop {0}".format(item_name)
        else:
            return "There is no {0} in your inventory".format(item_name)

    def equip_command(self, args):
        item_name = args[0] + "_" + args[1]
        inventory = self.var_handler.get('inventory_handler')
        equip = None
        for item in inventory.items:
            if item.name == item_name:
                equip = item
                break
        if equip is not None:
            if equip.category != "gear":
                return "You cannot equip that"
            inventory.equip(equip)
            return "You equip {0}".format(item_name)
        else:
            return "There is no {0} in your inventory".format(item_name)

    def move_command(self, args):
        #TODO: Add sleep/time to moveing
        location = self.var_handler.get('player').location
        area = self.var_handler.get('player').area
        if len(args) == 1:
            move = args[0]
            try:
                move = int(move)
                move = location.areas.keys()[move]
            except:
                pass
            if move in location.areas:
                if area.name == move:
                    return "That's where you are"
                else:
                    location.move(move)
                    return "You move to the {0}".format(move)
            else:
                if move not in location.areas:
                    return "That is not an area"
        else:
            areas = ""
            for area_name in location.areas:
                if area_name != area.name:
                    areas += area_name + ", "
            return "You can move to: {0}".format(areas).strip(", ")

    def travel_command(self, args):
        location = self.var_handler.get('player').location
        if len(args) == 1:
            move = args[0]
            try:
                move = int(move)
                move = location.location_map[move]
            except:
                pass
            if move in location.location_map:
                if location.name == move:
                    return "That's where you are"
                else:
                    location.travel(move)
                    return "You travel to the {0}".format(move)

    def buy_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        shop = player.area.get_object('npcs', 'shop')
        if shop is None:
            return "There is no shop here to buy from"
        if len(args) == 0:
            return shop.display()
        else:
            amount = 1 if len(args) == 2 else int(args[2])
            purchase = shop.buy(args[0] + "_" + args[1], amount)
            if purchase == 1:
                return "This shop does not have that item"
            elif purchase == 2:
                return "You do not have enough gold to buy that "
            else:
                inventory.add_item("*", "*", purchase)
                return "You buy {0}".format(args[0] + "_" + args[1])

    def sell_command(self, args):
        raise NotImplementedError

    def prospect_command(self, args):
        #TODO: add verbose
        mine = self.var_handler.get('player').area.get_object('places', 'mine')
        if mine is not None:
            return mine.prospect()
        else:
            return "No mine here to prospect"

    def mine_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        mine = player.area.get_object('places', 'mine')
        if mine is None:
            return "There is no mine here"
        ores = mine.mine(player.gathering_current)
        if ores == 1:
            return "You need level {0} to mine here".format(mine.level)
        elif ores == 2:
            return "You have mined all of ore you can for now, come back later"
        else:
            for ore_type in ores:
                try:
                    inventory.add_item("resources", "ores", ore_type, ores[ore_type])
                except ValueError:
                    return "You finish mining, but could not take all the ore with you"
            return "You finish mining"

    def cut_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        grove = player.area.get_object('places', 'grove')
        if grove is None:
            return "There is nothing here to cut"
        num = args[0]
        if int(num) > inventory.free_spaces():
            self.var_handler.get('status_handler').output("You can't hold that many, you'll cut as many as you can hold")
            num = str(inventory.free_spaces())
            if num == "0":
                return "You do not have room to hold any more logs"
        logs = grove.cut(player.gathering_current, num)
        if logs == 1:
            return "You need level {0} to cut these trees".format(grove.level)
        else:
            for log in logs:
                try:
                    inventory.add_item("resources", "logs", log, 1)
                except ValueError:
                    return "You finish cutting, but could not take all the logs with you"
            log_counts = {type:logs.count(type) for type in logs}
            cut_string = "You cut "
            for type in log_counts.keys():
                cut_string += str(log_counts[type]) + " " + type + "s, "
            return cut_string.strip(", ")

    def hunt_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        tracks = player.area.get_object('places', 'tracks')
        if tracks is None:
            return "There is nothing here to hunt"
        gain = tracks.hunt(player.hunting_current)
        if gain == 1:
            return "You do not have the level needed to hunt here"
        elif gain == 2:
            return "You have already hunted all you can here, come back later"
        else:
            meat_count = 0
            hide_count = 0
            meat = ""
            hide = ""
            for item in gain:
                try:
                    if "raw" in item:
                        meat_count += 1
                        meat = item
                        inventory.add_item("resources", "meats", item, 1)
                    else:
                        hide_count += 1
                        hide = item
                        inventory.add_item("resources", "hides", item, 1)
                except ValueError:
                    return "You finish hunting, but could not take all the animal with you"

            return "You killed the animal and got {0} {1} and {2} {3}".format(meat_count, meat, hide_count, hide)

    def farm_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        farm = player.area.get_object('places', 'farm')
        if farm is None:
            return "You cannot farm here"
        if len(args) == 0:
            args.append("")
        crop = farm.farm(player.farming_current, args[0])
        if crop == 1:
            return "This crop needs more time to grow"
        elif crop == 2:
            return "That is not a plant you can grow"
        elif crop == 3:
            return "You're farming level is not high enough to grow that"
        elif crop == 4:
            return "You plant the seeds, come back later to harvest"
        elif crop == 5:
            return "What do you want to grow?"
        elif crop == 6:
            return "You cannot grow that at this farm"
        for x in range(crop[1]):
            inventory.add_item("resources", "plants", crop[0], 1)
        return "You pick {0} {1}".format(crop[1], crop[0])

    def forage_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        field = player.area.get_object('places', 'field')
        if field is None:
            return "There are no plants here to forage from"
        fibers = field.forage(player.farming_current)
        if fibers == 1:
            return "You do not have the level needed to forage here"
        for x in range(fibers[1]):
            inventory.add_item("resources", "fibers", fibers[0], 1)

        return "You pick {0} {1}".format(fibers[1], fibers[0])

    def harness_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        rift = player.area.get_object('places', 'rift')
        if rift is None:
            return "There is no rift here to harness energy from"
        energy = rift.harness(player.magic_current)
        if energy == 1:
            return "You do not have the level needed to harness this rift"
        inventory.add_item("materials", "energy", energy[0], energy[1])
        player.area.remove_game_object(rift, "places")
        return "You harness {0} {1}".format(energy[1], energy[0])

    def spin_command(self, args):
        #TODO: add args, if given 1 arg and is number, ask which fiber
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        spinningwheel = player.area.get_object('stations', 'spinningwheel')
        if spinningwheel is None:
            return "There is no spinning wheel here"
        cloths = None
        spun_fibers = None
        if len(args) == 0:
            fibers = []
            for item in inventory.items:
                if item.type == "fiber":
                    fibers.append(item.name)
            cloths, spun_fibers = spinningwheel.spin(fibers)
        if cloths == []:
            return "No cloth could be created from your inventory"
        else:
            for cloth in spun_fibers:
                for item in inventory.items:
                    if item.name == cloth:
                        inventory.remove_item(item)
                        break
            for cloth in cloths:
                inventory.add_item("materials", "cloths", cloth, 1)
            return "You spin {0} fibers into {1} cloth".format(len(spun_fibers), len(cloths))

    def cook_command(self, args):
        #TODO: add args, if given 1 arg and is number, ask which meat
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        stove = player.area.get_object('stations', 'stove')
        if stove is None:
            return "There is nothing to cook on here"
        foods = None
        cooked_meats = None
        if len(args) == 0:
            meats = []
            for item in inventory.items:
                if item.type == "meat":
                    meats.append(item.name)
            foods, cooked_meats = stove.cook(meats)
        if foods == []:
            return "No food could be created from your inventory"
        else:
            for food in cooked_meats:
                for item in inventory.items:
                    if item.name == food:
                        inventory.remove_item(item)
                        break
            for food in foods:
                inventory.add_item("materials", "foods", food, 1)
            return "You cook {0} raw meat into {1} cooked meat".format(len(cooked_meats), len(foods))

    def smelt_command(self, args):
        #TODO: add args, if given 1 arg and is number, ask which ore
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        furnace = player.area.get_object('stations', 'furnace')
        if furnace is None:
            return "There is no furnace here"
        bars = None
        smelted_ores = None
        if len(args) == 0:
            ores = []
            for item in inventory.items:
                if item.type == "ore":
                    ores.append(item.name)
            if ores != []:
                bars, smelted_ores = furnace.smelt(ores)
            else:
                return "You have no ore you can smelt"
        if bars == []:
            return "No bars could be smelted from your inventory"
        else:
            for ore in smelted_ores:
                for item in inventory.items:
                    if item.name == ore:
                        inventory.remove_item(item)
                        break
            for bar in bars:
                inventory.add_item("materials", "bars", bar, 1)
            return "You smelt {0} ore(s) into {1} bar(s)".format(len(smelted_ores), len(bars))

    def mill_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        sawmill = player.area.get_object('stations', 'sawmill')
        if sawmill is None:
            return "There is nothing to mill logs with here"
        planks = None
        cut_logs = None
        if len(args) == 0:
            logs = []
            for item in inventory.items:
                if item.type == "log":
                    logs.append(item.name)
            planks, cut_logs = sawmill.mill(logs)
        elif len(args) >= 2:
            if len(args) == 3:
                amount = int(args[2])
                if amount == 0:
                    return "You sweat and toil and eventually are able to mill all {0} logs".format(amount)
            else:
                amount = inventory.max_items
            logs = []
            for item in inventory.items:
                if item.name == args[0] + "_" + args[1]:
                    logs.append(item.name)
                    if len(logs) == amount:
                        break
            planks, cut_logs = sawmill.mill(logs)
        if planks == []:
            return "No planks could be created from your inventory"
        else:
            for log in cut_logs:
                for item in inventory.items:
                    if item.name == log:
                        inventory.remove_item(item)
                        break
            for plank in planks:
                inventory.add_item("materials", "planks", plank, 1)
            return "You cut {0} log(s) into {1} plank(s)".format(len(cut_logs), len(planks))

    def tan_command(self, args):
        #TODO: add args, if given one arg and is number, ask which hide type
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        tannery = player.area.get_object('stations', 'tannery')
        if tannery is None:
            return "There is no tannery here"
        leathers = None
        tanned_hides = None
        if len(args) == 0:
            hides = []
            for item in inventory.items:
                if item.type == "hide":
                    hides.append(item.name)
            leathers, tanned_hides = tannery.tan(hides)
        if leathers == []:
            return "No leather could be created from your inventory"
        else:
            for hide in tanned_hides:
                for item in inventory.items:
                    if item.name == hide:
                        inventory.remove_item(item)
                        break
            for leather in leathers:
                inventory.add_item("materials", "leathers", leather, 1)
            return "You tan {0} hide into {1} leather".format(len(tanned_hides), len(leathers))

    def grind_command(self, args):
        #TODO: add args, if given one arg and is number, ask which plant type
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        pestle = player.area.get_object('stations', 'pestle')
        if pestle is None:
            return "There is nothing to grind with here"
        ingredients = None
        ground_plants = None
        if len(args) == 0:
            ingredients = []
            for item in inventory.items:
                if item.type == "plant":
                    ingredients.append(item.name)
            ingredients, ground_plants = pestle.grind(ingredients)
        if ingredients == []:
            return "No ingredients could be created from your inventory"
        else:
            for plant in ground_plants:
                for item in inventory.items:
                    if item.name == plant:
                        inventory.remove_item(item)
                        break
            for plant in ingredients:
                inventory.add_item("materials", "ingredients", plant, 1)
            return "You grind {0} plants into {1} ingredients".format(len(ground_plants), len(ingredients))

    def smith_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        anvil = player.area.get_object('stations', 'anvil')
        if anvil is None:
            return "There is no anvil here"
        materials = []
        for item in inventory.items:
            if item.category == "material":
                materials.append(item.name)
        if len(args) == 0:
            items =  anvil.list_makeable_recipes(materials)
            items_string = "You can make:\n"
            if items == []:
                items_string += "nothing"
            else:
                for item in items:
                    items_string += item + ", "
                    if len(items_string) > 40:
                        items_string += "\n"
            return items_string.strip(", ")
        else:
            item_name = ""
            for word in args:
                item_name += word + " "
            item_name = item_name.strip()
            item_name = item_name.replace(" ", "_")

            result = anvil.smith(materials, item_name)
            if result == 1:
                return "You do not know how to make that item (if it even exists)"
            elif result == 2:
                return "You do not have the materials to make that"
            else:
                new_item = result[0]
                smithed_materials = result[1]
                for material in smithed_materials:
                    for item in inventory.items:
                        if item.name == material:
                            inventory.remove_item(item)
                            break
                inventory.add_item("gear", "*", new_item, 1)
            return "You have created {0}".format(new_item)

    def brew_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        cauldron = player.area.get_object('stations', 'cauldron')
        if cauldron is None:
            return "There is no cauldron here to brew in"
        materials = []
        for item in inventory.items:
            if item.category == "material":
                materials.append(item.name)
        if len(args) == 0:
            items =  cauldron.list_brewable_recipes(materials)
            items_string = "You can make: "
            if items == []:
                items_string += "nothing--"
            else:
                for item in items:
                    items_string += item + ", "
            return items_string.strip(", ")
        else:
            item_name = ""
            for word in args:
                item_name += word + " "
            item_name = item_name.strip()
            item_name = item_name.replace(" ", "_")

            result = cauldron.brew(materials, item_name)
            if result == 1:
                return "You do not know how to brew that item (if it even exists)"
            elif result == 2:
                return "You do not have the materials to make that"
            else:
                new_item = result[0]
                brewed_materials = result[1]
                for material in brewed_materials:
                    for item in inventory.items:
                        if item.name == material:
                            inventory.remove_item(item)
                            break
                inventory.add_item("consumables", "potions", new_item, 1)
            return "You have created {0}".format(new_item)

    def weave_command(self, args):
        player = self.var_handler.get('player')
        inventory = self.var_handler.get('inventory_handler')
        focus = player.area.get_object('stations', 'focus')
        if focus is None:
            return "There is no focus here to weave with"
        materials = []
        for item in inventory.items:
            if item.category == "material":
                materials.append(item.name)
        if len(args) == 0:
            items = focus.list_weaveable_recipes(materials)
            items_string = "You can make:\n"
            if items == []:
                items_string += "nothing--"
            else:
                for item in items:
                    items_string += item + ", "
                    if len(items_string) > 40:
                        items_string += "\n"
            return items_string.strip(", ")
        else:
            item_name = ""
            for word in args:
                item_name += word + " "
            item_name = item_name.strip()
            item_name = item_name.replace(" ", "_")

            result = focus.weave(materials, item_name)
            if result == 1:
                return "You do not know how to make that item (if it even exists)"
            elif result == 2:
                return "You do not have the materials to make that"
            else:
                new_item = result[0]
                wovern_materials = result[1]
                for material in wovern_materials:
                    for item in inventory.items:
                        if item.name == material:
                            inventory.remove_item(item)
                            break
                inventory.add_item("consumables", "*", new_item, 1)
            return "You have created {0}".format(new_item)

    def drink_command(self, args):
        item_name = args[0] + "_" + args[1]
        inventory = self.var_handler.get('inventory_handler')
        potion = None
        for item in inventory.items:
            if item.name == item_name:
                potion = item
                break
        if potion is not None:
            drunk = potion.drink(self.var_handler.get('player'), self.var_handler.get('time_handler'))
            if drunk == 1:
                return "You cannot drink that"
            elif drunk == 2:
                return "You are already under the effects of that potion"
            else:
                inventory.remove_item(potion)
                return drunk
        else:
            return "There is no {0} in your inventory".format(item_name)

    def enchant_command(self, args):
        item_name = args[0] + "_" + args[1]
        enchantment_name = args[2] + "_" + args[3]
        inventory = self.var_handler.get('inventory_handler')
        enchantment = None
        gear = None
        for item in inventory.items:
            if item.name == enchantment_name:
                enchantment = item
                break
        for item in inventory.items:
            if item.name == item_name:
                gear = item
                break
        if enchantment is not None and gear is not None:
            if gear.category != "gear":
                return "You can only enchant worn items"
            if gear.enchantment is not None:
                return "That item is already enchanted\nRemove the current enchantment before adding a new one"
            inventory.remove_item(enchantment)
            for buff in enchantment.stats:
                gear.stats.append(buff)
                gear.enchantment = enchantment
                gear.frame_color = enchantment.frame_color
                return "You enchant your {0} with a {1}".format(gear.name, enchantment.name)
        else:
            return "Not all of those items are in you inventory\n(you must unequip gear before enchanting it)"

    def look_command(self, args):
        player = self.var_handler.get('player')
        area = player.area
        if len(args) == 0:
            return area.description
        else:
            for category in area.game_objects:
                for game_object in area.game_objects[category]:
                    if game_object.name == args[0]:
                        return game_object.description
        return "There is no '{0}' to look at".format(args[0])

    def clear_command(self, args):
        return self.var_handler.get('io_handler').clear_screen()

    def exit_command(self, args):
        exit(0)

class Command():
    def __init__(self, name, num_args, usage, info, color, function):
        self.name = name
        self.num_args = num_args
        self.usage = usage
        self.info = info
        self.color = color
        self.function = function

    def run(self, args):
        return (self.function(args).replace("_", " "), curses.color_pair(self.color))