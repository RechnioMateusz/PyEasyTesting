import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '_logic'))
sys.path.append(os.path.join(current_path, 'gui_elements'))
