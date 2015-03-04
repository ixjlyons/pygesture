import sys
import os

# settings that need to be specified in the config
config_options = [
    "num_repeats",
    "trial_duration",
    "prompt_times",
    "inter_trial_timeout",
    "data_path",
    "vrep_path",
    "conditioner",
    "windower",
    "feature_extractor",
    "post_processor",
    "arm_sensors",
    "leg_sensors",
    "channels",
    "probe_channel",
    "daq",
    "arm_gestures",
    "leg_gestures"
    "results_sid_arm",
    "results_sid_leg"
]


class Config(object):
    
    def __init__(self, filepath):
        sys.path.insert(0, os.path.dirname(filepath))
        config = __import__(os.path.basename(filepath)[:-3])

        for option in config_options:
            c = getattr(config, option, None)
            setattr(self, option, c)

