import os
from pygesture import util
from pygesture import pipeline
from pygesture import features
from pygesture import processing
from pygesture import daq
from pygesture import control
from pygesture import experiment

"""
some things for local use
"""
# sampling frequency for the DAQ [Hz]
f_samp = 5120
# frequency of signals for processing [Hz]
f_proc = 2560
# cutoff frequencies for bandpass conditioning filter [Hz]
f_cutoff = [8, 512]
# order of conditioning filter
filt_order = 4
# voltage input range for the DAQ
input_range = 2

# length of sliding window [ms]
window_length = 150
# amount of overlap between adjacent windows [ms]
window_overlap = 100


"""
attributes picked up by pygesture.config
"""
# number of times to repeat each gesture during training
num_repeats = 3
# length of each trial during training [seconds]
trial_duration = 6
# gesture onset and offset times for training [seconds]
prompt_times = (2, 5)
# time between trials in training [seconds]
inter_trial_timeout = 3

# path to save/load recordings and feature CSVs
data_path = os.path.expanduser('~/pygesture-data/online')
# path to v-rep (needed for simulation package)
vrep_path = os.path.expanduser('~/usr/vrep/vrep-3.2.1')
# port that the v-rep is listening on (in remoteApiConnections.txt)
vrep_port = 20013

# sensor mappings
arm_sensors = [
    util.Sensor(0, "ECR", description="extensor carpi radialis brevis"),
    util.Sensor(1, "ED", description="extensor digitorum"),
    util.Sensor(2, "EPL", description="extensor pollicis longus"),
    util.Sensor(3, "FDS", description="flexor digitorum superficialis"),
    util.Sensor(4, "FCR", description="flexor carpi radialis"),
    util.Sensor(5, "PT", description="pronator teres")
]
leg_sensors = [
    util.Sensor(0, "TA", description="tibialis anterior"),
    util.Sensor(1, "PL", description="peroneus longus"),
    util.Sensor(2, "GL", description="gastrocnemius lateralis"),
    util.Sensor(3, "EHL", description="extensor hallucis longus"),
    util.Sensor(4, "EDL", description="extensor digitorum longus"),
    util.Sensor(5, "FDL", description="flexor digitorum longus"),
]

channels = [s.channel for s in arm_sensors]
probe_channel = 6

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
    daq = daq.MccDaq(
        rate=f_samp,
        input_range=input_range,
        channel_range=(min(channels), max(channels)),
        samples_per_read=int(f_samp*(window_length-window_overlap)/1000)
    )
except ValueError:
    daq = daq.Daq(
        rate=f_samp,
        input_range=input_range,
        channel_range=(min(channels), max(channels)),
        samples_per_read=int(f_samp*(window_length-window_overlap)/1000)
    )

conditioner = pipeline.Conditioner(
    order=filt_order,
    f_cut=f_cutoff,
    f_samp=f_samp,
    f_down=f_proc
)

windower = pipeline.Windower(
    length=int(f_proc*window_length/1000),
    overlap=int(f_proc*window_overlap/1000)
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

post_processor = processing.Processor(
    conditioner=conditioner,
    windower=windower,
    feature_extractor=feature_extractor,
    rest_bounds=(int(1.0*f_proc), int(1.5*f_proc)),
    gesture_bounds=(int(2.0*f_proc), int(4.0*f_proc))
)

controller = control.DBVRController(
    mapping={g.label: g.action for g in gestures},
    ramp_length=10,
    boosts=0.5
)

tac_sessions = {
    '1. 3-1 a':
        experiment.TACSession(
            [g for g in gestures if g.dof in [1, 2, 3]],
            simul=1, rep=4, timeout=15, tol=10, dwell=2),
    '2. 3-1 b':
        experiment.TACSession(
            [g for g in gestures if g.dof in [0, 2, 3]],
            simul=1, rep=4, timeout=15, tol=10, dwell=2),
    '3. 3-3 a':
        experiment.TACSession(
            [g for g in gestures if g.dof in [1, 2, 3]],
            simul=3, rep=2, timeout=30, tol=10, dwell=2),
    '4. 3-3 b':
        experiment.TACSession(
            [g for g in gestures if g.dof in [0, 2, 3]],
            simul=3, rep=2, timeout=30, tol=10, dwell=2),
    '5. 4-1':
        experiment.TACSession(
            [g for g in gestures if g.dof is not None],
            simul=1, rep=4, timeout=15, tol=10, dwell=2)
}
