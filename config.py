import os
import collections

from sklearn.lda import LDA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from pygesture import util
from pygesture import pipeline
from pygesture import features
from pygesture import daq
from pygesture import control
from pygesture import experiment
from pygesture.analysis import processing

from pygesture.ui import train
from pygesture.ui import test

"""
some things for local use
"""

# default data acquisition system parameters
trigno_daq = {
    'f_samp': 2000,
    'f_proc': 2000,
    'm': 1,
    'f_cutoff': [10, 500],
    'filt_order': 2,
    'input_range': 1,
    'window_length': 432,
    'window_overlap': 216,
    'probe_channel': 0
}

# fallback data acquistion system parameters
mcc_daq = {
    'f_samp': 5120,
    'f_proc': 2560,
    'm': 2,
    'f_cutoff': [8, 512],
    'filt_order': 2,
    'input_range': 2,
    'window_length': 512,
    'window_overlap': 256,
    'probe_channel': 7
}


"""
attributes picked up by pygesture.config
"""
# number of times to repeat each gesture during training
num_repeats = 4
# length of each trial during training [seconds]
trial_duration = 6
# gesture onset and offset times for training [seconds]
prompt_times = (2, 5)
# time between trials in training [seconds]
inter_trial_timeout = 3

# path to save/load recordings and feature CSVs
data_path = os.path.expanduser(
    os.path.join('~', 'pygesture-data', 'tactest2'))

# sensor mappings
sensors = [
    util.Sensor(0, "ECR/TA"),
    util.Sensor(1, "ED/PL"),
    util.Sensor(2, "EPL/GL"),
    util.Sensor(3, "FDS/EHL"),
    util.Sensor(4, "FCR/EDL"),
    util.Sensor(5, "PT/FDL")
]

channels = [s.channel for s in sensors]

gestures = [
    util.Gesture(0, "NC", "no-contraction"),
    util.Gesture(1, "CF", "closed-fist", dof=3),
    util.Gesture(2, "FP", "forearm-pronation", dof=1),
    util.Gesture(3, "FS", "forearm-supination", dof=1),
    util.Gesture(4, "OH", "open-hand", dof=3),
    util.Gesture(5, "RD", "radial-deviation", dof=0, action="elbow-flexion"),
    util.Gesture(7, "UD", "ulnar-deviation", dof=0, action="elbow-extension"),
    util.Gesture(8, "WE", "wrist-extension", dof=2),
    util.Gesture(9, "WF", "wrist-flexion", dof=2)
]

try:
    daq_st = trigno_daq
    daq = daq.TrignoDaq(
        channel_range=(min(channels), max(channels)),
        samples_per_read=
            daq_st['m']*(daq_st['window_length']-daq_st['window_overlap'])
    )
except:
    try:
        daq_st = mcc_daq
        daq = daq.MccDaq(
            rate=daq_st['f_samp'],
            input_range=daq_st['input_range'],
            channel_range=(min(channels), max(channels)),
            samples_per_read=
                daq_st['m']*(daq_st['window_length']-daq_st['window_overlap'])
        )
    except:
        daq = daq.Daq(
            rate=daq_st['f_samp'],
            input_range=daq_st['input_range'],
            channel_range=(min(channels), max(channels)),
            samples_per_read=
                daq_st['m']*(daq_st['window_length']-daq_st['window_overlap'])
        )

probe_channel = daq_st['probe_channel']

conditioner = pipeline.Conditioner(
    order=daq_st['filt_order'],
    f_cut=daq_st['f_cutoff'],
    f_samp=daq_st['f_samp'],
    f_down=daq_st['f_proc']
)

windower = pipeline.Windower(
    length=daq_st['window_length'],
    overlap=daq_st['window_overlap']
)

feature_extractor = features.FeatureExtractor(
    [
        features.MAV(),
        features.WL(),
        features.ZC(thresh=0.001),
        features.SSC(thresh=0.001)
    ],
    len(channels)
)

learner = pipeline.Classifier(
    Pipeline([
        ('preproc', StandardScaler()),
        ('clf', LDA())])
)

post_processor = processing.Processor(
    conditioner=conditioner,
    windower=windower,
    feature_extractor=feature_extractor,
    rest_bounds=None,
    gesture_bounds=(int((prompt_times[0]+0.5)*daq_st['f_proc']),
                    int((prompt_times[1]-0.5)*daq_st['f_proc']))
)

controller = control.DBVRController(
    mapping={g.label: g.action for g in gestures},
    ramp_length=10
)

tac_sessions = {
    '3 active, 1 target':
        experiment.TACSession(
            [g for g in gestures if g.dof in [1, 2, 3]],
            simul=1, rep=2, timeout=15, dist=60, tol=10, dwell=2),
    '3 active, 2 target':
        experiment.TACSession(
            [g for g in gestures if g.dof in [1, 2, 3]],
            simul=(1, 2), rep=1, timeout=20, dist=60, tol=10, dwell=2),
    '4 active, 1 target':
        experiment.TACSession(
            [g for g in gestures if g.dof is not None],
            simul=1, rep=2, timeout=15, dist=60, tol=10, dwell=2),
    '4 active, 2 target':
        experiment.TACSession(
            [g for g in gestures if g.dof is not None],
            simul=(1, 2), rep=1, timeout=20, dist=60, tol=10, dwell=2)
}

ui_tabs = collections.OrderedDict()
ui_tabs['Train'] = train.TrainWidget
ui_tabs['Test'] = test.TestWidget
