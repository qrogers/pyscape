import os
import re
import importlib

#import all of the unit files dynamically so that the unit handler can spawn any unit without an import line for each one
for file in os.listdir('bin/game_objects/units'):
    if re.match("[a-z]+\.py$", file) is not None:
        importlib.import_module("bin.game_objects.units." + file.replace(".py", ""))
