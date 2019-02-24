import os
import sys
from . import my_widgets
from . import my_windows

current_path = os.path.dirname(os.path.realpath(__file__))
for _file in os.listdir(current_path):
    path = os.path.join(current_path, _file)
    if(os.path.isdir(path)):
        sys.path.append(path)
