from bin.game_objects.places.place import Place
from random import randint

class Tracks(Place):
    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Tracks, self).__init__(number, area, name, description, difficulty, level, info)
        #Number of ticks and waits until prey is caught
        self.duration = self.info['duration']
        #Kind of animal that you hunt, determines yield
        self.prey = self.info['prey']
        #Amount of each resource you get
        self.gain = self.info['gain']
        #Number of times these tracks can be hunted
        self.amount = self.info['amount']

        self.max_amount = self.amount

        self.time.register_move_event(self.move)

        self.increment = 0

        self.xp_bounty = {"deer"   : 110,
                          "lizard" : 220,
                          "tiger"  : 330,
                          "wyvern" : 440,
                          "demon"  : 550,
                          "dragon" : 660,
                          "black"  : 660}

        self.animals = {"deer"   : ("deer_hide"  , "raw_venison"),
                        "lizard" : ("lizard_hide", "raw_lizard"),
                        "tiger"  : ("tiger_hide" , "raw_tiger"),
                        "demon"  : ("demon_hide" , "raw_demon"),
                        "dragon" : ("dragon_hide", "raw_dragon"),
                        "black"  : ("black_hide" , "black_meat")}

        self.chars = [".", "!", ".", ".", "?"]

    def hunt(self, level):
        if level >= self.level:
            if self.amount > 0:
                self.status.start_sequence()
                self.status.output("You begin tracking the {0}".format(self.prey))
                self.time.sleep(1)
                self.time.tick(1)
                time_per_step = self.difficulty - level
                if time_per_step < 1:
                    time_per_step = 1
                for step in range(self.duration + randint(-2, 2)):
                    self.time.sleep(time_per_step)
                    output = ""
                    for x in range(1, randint(4, 8)):
                        output += self.chars[randint(0, len(self.chars) - 1)]
                    self.status.slow_output(output, self.time)
                    self.time.tick(1)
                animal = self.animals[self.prey]
                self.amount -= 1
                self.time.sleep(2)
                self.status.output("You finally catch your prey")
                self.player.gain_xp("hunting", self.xp_bounty[self.prey])
                self.status.end_sequence()
                gain = []
                for item in range(self.gain[0]):
                    gain.append(animal[0])
                for item in range(self.gain[1]):
                    gain.append(animal[1])
                return gain
            else:
                return 2
        else:
            return 1

    def move(self):
        self.increment += 1
        if self.increment >= 5:
            self.increment = 0
            self.amount += 1
            if self.amount > self.max_amount:
                self.amount = self.max_amount