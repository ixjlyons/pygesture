import sys
import os

config_options = [
    "f_samp",
    "f_proc",
    "f_cutoff",
    "filt_order",
    "input_range",
    "window_length",
    "window_overlap"
    "data_path",
    "vrep_path",
    "arm_sensors",
    "leg_sensors",
    "arm_gestures",
    "leg_gestures"
]


class Config(object):
    
    def __init__(self, filepath):
        sys.path.insert(0, os.path.dirname(filepath))
        config = __import__(os.path.basename(filepath)[:-3])

        for option in config_options:
            c = getattr(config, option, None)
            setattr(self, option, c)

