import os
import sys
from . import settings_agent
from . import files_creator
from . import test_detector
from . import linker

current_path = os.path.dirname(os.path.realpath(__file__))
for _file in os.listdir(current_path):
    path = os.path.join(current_path, _file)
    if(os.path.isdir(path)):
        sys.path.append(path)
