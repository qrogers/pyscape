import os
import re
import importlib

for file in os.listdir('bin/game_objects/npcs'):
    if re.match("[a-z]+\.py$", file) is not None:
        importlib.import_module("bin.game_objects.npcs." + file.replace(".py", ""))
