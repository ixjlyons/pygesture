import sys
import os

# settings that need to be specified in the config
config_options = [
    "f_samp",
    "f_proc",
    "f_cutoff",
    "filt_order",
    "input_range",
    "window_length",
    "window_overlap",
    "num_repeats",
    "samples_per_read",
    "seconds_per_prompt",
    "gesture_time",
    "inter_trial_timeout",
    "reads_per_prompt",
    "data_path",
    "vrep_path",
    "conditioner",
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

