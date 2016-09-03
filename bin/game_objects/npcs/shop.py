from bin.game_objects.npcs.npc import NPC
from bin.item import Item

class Shop(NPC):
    def __init__(self, number, area, name, description, info):
        super(Shop, self).__init__(number, area, name, description)
        #Items for sale
        self.wares = info['wares']

    def display(self):
        items_str = ""
        self.wares.sort(key=lambda ware: ware[0])
        for listing in self.wares:
            num_cost = listing[1].split(",")
            items_str += "{0} {1} for {2} gold each\n".format(num_cost[0], listing[0], num_cost[1])
        return items_str.strip("\n")

    def buy(self, item):
        ware = None
        for listing in self.wares:
            if item == listing[0]:
                ware = listing
        if ware is None:
            # Item not in shop
            return 1
        if self.inventory.gold < int(ware[1].split(",")[1]):
            # Not enough gold to buy
            return 2
        self.inventory.change_gold(int(ware[1].split(",")[1]) * -1)
        num = int(ware[1].split(",")[0])
        num -= 1
        self.wares.remove(ware)
        if num > 0:
            ware = (ware[0], str(num) + "," + ware[1].split(",")[1])
            self.wares.append(ware)
        return ware[0]

    def sell(self):
        raise NotImplementedError