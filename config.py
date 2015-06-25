import os
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

# sensor mappings
# channel_number : (
#     ('arm_abbrv', 'arm_description')
#     ('leg_abbrv', 'leg_description')
# )
sensors = {
    0: (
        ('ECR', 'extensor carpi radialis brevis'),
        ('TA', 'tibialis anterior')
    ),
    1: (
        ('ED', 'extensor digitorum'),
        ('PL', 'peroneus longus')
    ),
    2: (
        ('EPL', 'extensor pollicis longus'),
        ('GL', 'gastrocnemius lateralis')
    ),
    3: (
        ('FDS', 'flexor digitorum superficialis'),
        ('EHL', 'extensor hallucis longus')
    ),
    4: (
        ('FCR', 'flexor carpi radialis'),
        ('EDL', 'extensor digitorum longus')
    ),
    5: (
        ('PT', 'pronator teres'),
        ('FDL', 'flexor digitorum longus')
    )
}

# gesture mappings
# label : (
#     ('arm_abbrv', 'arm_description'),
#     ('leg_abbrv', 'leg_description'),
#     'simulation_action',
#     dof)
# }
gestures = {
    0: (
        ('NC', 'no-contraction'),
        ('NC', 'no-contraction'),
        'no-contraction',
        -1),
    1: (
        ('CF', 'closed-fist'),
        ('TF', 'toe-flexion'),
        'closed-fist',
        0),
    2: (
        ('FP', 'forearm-pronation'),
        ('FE', 'foot-eversion'),
        'forearm-pronation',
        2),
    3: (
        ('FS', 'forearm-supination'),
        ('FI', 'foot-inversion'),
        'forearm-supination',
        2),
    4: (
        ('OH', 'open-hand'),
        ('TE', 'toe-extension'),
        'open-hand',
        0),
    5: (
        ('RD', 'radial-deviation'),
        ('AD', 'foot-adduction'),
        'elbow-flexion',
        3),
    7: (
        ('UD', 'ulnar-deviation'),
        ('AB', 'foot-abduction'),
        'elbow-extension',
        3),
    8: (
        ('WE', 'wrist-extension'),
        ('DF', 'dorsiflexion'),
        'wrist-extension',
        1),
    9: (
        ('WF', 'wrist-flexion'),
        ('PF', 'plantarflexion'),
        'wrist-flexion',
        1)
}

# {'gesture': dof}
dofs3a = {
    val[2]: val[3] for (key, val) in gestures.items() if val[3] in [0, 1, 2]
}
dofs3b = {
    val[2]: val[3] for (key, val) in gestures.items() if val[3] in [0, 1, 3]
}
dofs4 = {
    val[2]: val[3] for (key, val) in gestures.items() if val[3] in [0, 1, 2, 3]
}

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
# channel_number : ('abbrv', 'muscle')
arm_sensors = {key: val[0] for (key, val) in sensors.items()}
leg_sensors = {key: val[1] for (key, val) in sensors.items()}

channels = sorted(list(arm_sensors))

probe_channel = 6

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

# gesture mappings
# label: ('abbrv', 'description')
arm_gestures = {key: val[0] for (key, val) in gestures.items()}
leg_gestures = {key: val[1] for (key, val) in gestures.items()}

# simulation mapping
# label : 'action'
vrep_actions = {key: val[2] for (key, val) in gestures.items()}

controller = control.DBVRController(
    mapping=vrep_actions,
    ramp_length=5,
    boosts=0.5
)

tac_sessions = {
    '1. 3-1 a':
        experiment.TACSession(
            dofs3a, simul=1, rep=4, timeout=15, tol=10, dwell=2),
    '2. 3-1 b':
        experiment.TACSession(
            dofs3b, simul=1, rep=4, timeout=15, tol=10, dwell=2),
    '3. 3-3 a':
        experiment.TACSession(
            dofs3a, simul=3, rep=2, timeout=30, tol=10, dwell=2),
    '4. 3-3 b':
        experiment.TACSession(
            dofs3b, simul=3, rep=2, timeout=30, tol=10, dwell=2),
    '5. 4-1':
        experiment.TACSession(
            dofs4, simul=1, rep=4, timeout=15, tol=10, dwell=2)
}
