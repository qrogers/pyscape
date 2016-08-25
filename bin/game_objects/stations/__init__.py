import os
import re
import importlib

for file in os.listdir('bin/game_objects/stations'):
    if re.match("[a-z]+\.py$", file) is not None:
        importlib.import_module("bin.game_objects.stations." + file.replace(".py", ""))
