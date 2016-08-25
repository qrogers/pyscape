from time import sleep

DEBUG_TIME_SCALE = 1

#TODO: Add stat regen

class TimeHandler():
    def __init__(self):
        self.ticks = 0
        self.moves = 0
        self.tick_events = []
        self.move_events = []
        self.events_to_remove = []

    def tick(self, amount=1):
        if amount < 1:
            raise ValueError("Cannot tick less than 1")
        self.ticks += 1
        events = self.tick_events[:]
        for event in events:
            event()
        if amount - 1 > 0:
            self.tick(amount - 1)

    def move(self):
        self.moves += 1
        self.tick(1)
        for event in self.move_events:
            event()

    def register_tick_event(self, event):
        self.tick_events.append(event)

    def deregister_tick_event(self, event):
        self.tick_events.remove(event)

    def register_move_event(self, event):
        self.move_events.append(event)

    def deregister_move_event(self, event):
        self.move_events.remove(event)

    def sleep(self, duration):
        sleep(duration * DEBUG_TIME_SCALE)
