from bin.game_objects.places.place import Place

from random import randint

class Grove(Place):
    def __init__(self, number, area, name, description, difficulty, level, info):
        super(Grove, self).__init__(number, area, name, description, difficulty, level, info)
        #Types of logs that can be gotten from the grove
        self.logs = info['logs']
        #Time to acquire each log
        self.wait = info['wait']
        #Chance to receive each log
        self.odds = info['odds']

        self.xp_bounty = {"oak_log"    : 10,
                          "maple_log"  : 17,
                          "willow_log" : 25,
                          "alder_log"  : 34,
                          "elder_log"  : 44,
                          "ebony_log"  : 55,
                          "imbued_log" : 55}

    def cut(self, level, amount):
        if level >= self.level:
            level_boost = self.difficulty - level
            cut_logs = []
            self.status.start_sequence()
            self.status.output("You enter the grove and begin to look for trees to cut")
            self.time.tick(1)
            self.time.sleep(5)
            self.status.output("You fell some trees and cut them into logs")
            self.time.sleep(5)
            self.time.tick(2)
            for x in range(int(amount)):
                i = len(self.logs) - 1
                while i >= 0:
                    if randint(0, 100) <= self.odds[i] - level_boost:
                        self.time.sleep(self.wait)
                        self.status.output("You cut a {0}".format(self.logs[i].replace("_", " ")))
                        self.player.gain_xp("gathering", self.xp_bounty[self.logs[i]])
                        time_per_log = self.difficulty - int(level / 10)
                        if time_per_log < 1:
                            time_per_log = 1
                        self.time.tick(time_per_log)
                        cut_logs.append(self.logs[i])
                        break
                    i -= 1
            self.time.sleep(3)
            self.time.tick(1)
            self.status.output("You have cut the desired amount of logs and leave the grove")
            self.status.end_sequence()
            return cut_logs
        else:
            return 1