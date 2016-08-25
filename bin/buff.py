class Buff():
    def __init__(self, name, skill, amount, duration, player, time_handler):
        self.name = name
        self.display_name = (name[:1].upper() + name[1:]).replace("_", " ")
        self.skill = skill
        self.amount = amount
        self.duration = duration
        self.player = player
        self.time = time_handler

        self.buff_effects = self.BuffEffects(self.player)

        if self.duration > 0:
            self.time.register_tick_event(self.tick)

    def tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.player.remove_buff(self)

    def apply(self):
        try:
            self.player.buff_skill(self.skill, self.amount)
        except AttributeError:
            self.buff_effects.buff_effects[self.skill]("apply", self.amount)
        if self.duration == 0:
            self.player.remove_buff(self)

    def remove(self):
        try:
            self.player.buff_skill(self.skill, self.amount * -1)
            if self.tick in self.time.tick_events:
                self.time.deregister_tick_event(self.tick)
        except AttributeError:
            self.buff_effects.buff_effects[self.skill]("remove", self.amount)

    class BuffEffects():
        def __init__(self, player):
            self.player = player
            self.buff_effects = {"heal" : self.heal}

        def heal(self, action, amount):
            if action == "apply":
                self.player.health_current += amount
                if self.player.health_current > self.player.health_level:
                    self.player.health_current = self.player.health_level
            elif action == "remove":
                pass