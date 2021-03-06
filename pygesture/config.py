import sys
import os

# settings that need to be specified in the config
config_options = [
    "num_repeats",
    "trial_duration",
    "prompt_times",
    "inter_trial_timeout",
    "data_path",
    "conditioner",
    "windower",
    "feature_extractor",
    "learner",
    "post_processor",
    "sensors",
    "channels",
    "probe_channel",
    "daq",
    "gestures",
    "controller",
    "tac_sessions",
    "ui_tabs"
]


class Config(object):

    def __init__(self, filepath):
        sys.path.insert(0, os.path.dirname(filepath))
        config = __import__(os.path.basename(filepath)[:-3])

        for option in config_options:
            c = getattr(config, option, None)
            setattr(self, option, c)
