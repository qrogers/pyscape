class Buff():
    def __init__(self, name, skill, amount, duration, player, time_handler):
        self.name = name
        self.display_name = (name[:1].upper() + name[1:]).replace("_", " ")
        self.skill = skill
        self.amount = amount
        self.duration = duration
        self.player = player
        self.time = time_handler

        self.buff_effect = None

        self.buff_effects = self.BuffEffects(self.player, self)

        if self.duration > 0:
            self.time.register_tick_event(self.tick)

    def tick(self):
        self.duration -= 1
        if self.buff_effect is not None:
            self.buff_effect()
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
        def __init__(self, player, buff):
            self.player = player
            self.buff_effects = {"heal" : self.heal,
                                 "restore" : self.restore,
                                 "refresh" : self.refresh}
            self.buff = buff

        def heal(self, action, amount):
            if action == "apply":
                self.player.health_current += amount
                if self.player.health_current > self.player.health_level:
                    self.player.health_current = self.player.health_level
                self.player.update_skill_window()
            elif action == "remove":
                pass

        def restore(self, action, amount):
            def tick_heal():
                if self.player.health_current < self.player.health_level and self.buff.duration % 2 == 0:
                        self.player.health_current += amount
                        if self.player.health_current > self.player.health_level:
                            self.player.health_current = self.player.health_level
                self.player.update_skill_window()
            if action == "apply":
                self.buff.buff_effect = tick_heal
            elif action == "remove":
                self.buff.buff_effect = None

        def refresh(self, action, amount):
            def tick_magic():
                if self.player.mgaic_current < self.player.magic_level and self.buff.duration % 2 == 0:
                        self.player.magic_current += amount
                self.player.update_skill_window()
            if action == "apply":
                self.buff.buff_effect = tick_magic
            elif action == "remove":
                self.buff.buff_effect = None