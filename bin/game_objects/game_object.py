class GameObject(object):
    def __init__(self, number, area, name, description):
        self.class_name = self.__class__.__name__.lower()
        self.number = number
        self.display_name = name
        self.name = name
        self.area = area
        self.var_handler =  self.area.var_handler
        self.status = self.var_handler.get('status_handler')
        self.time = self.var_handler.get('time_handler')
        self.inventory = self.var_handler.get('inventory_handler')
        self.player = self.var_handler.get('player')
        self.description = description