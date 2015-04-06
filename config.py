import os
from pygesture import pipeline
from pygesture import features
from pygesture import processing
from pygesture import daq
from pygesture import control

"""
some things for local use
"""
# sampling frequency for the DAQ [Hz]
f_samp = 4096
# frequency of signals for processing [Hz]
f_proc = 2048
# cutoff frequencies for bandpass conditioning filter [Hz]
f_cutoff = [8, 512]
# order of conditioning filter
filt_order = 4
# voltage input range for the DAQ
input_range = 2

# length of sliding window [s]
window_length = 0.250
# amount of overlap between adjacent windows [s]
window_overlap = 0

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
#     'simulation_action' )
gestures = {
    0: (
        ('NC', 'no-contraction'),
        ('NC', 'no-contraction'),
        'no-contraction'),
    1: (
        ('CF', 'closed-fist'),
        ('TF', 'toe-flexion'),
        'closed-fist'),
    2: (
        ('FP', 'forearm-pronation'),
        ('FE', 'foot-eversion'),
        'forearm-pronation'),
    3: (
        ('FS', 'forearm-supination'),
        ('FI', 'foot-inversion'),
        'forearm-supination'),
    4: (
        ('OH', 'open-hand'),
        ('TE', 'toe-extension'),
        'open-hand'),
    5: (
        ('RD', 'radial-deviation'),
        ('AD', 'foot-adduction'),
        'elbow-flexion'),
    7: (
        ('UD', 'ulnar-deviation'),
        ('AB', 'foot-abduction'),
        'elbow-extension'),
    8: (
        ('WE', 'wrist-extension'),
        ('DF', 'dorsiflexion'),
        'wrist-extension'),
    9: (
        ('WF', 'wrist-flexion'),
        ('PF', 'plantarflexion'),
        'wrist-flexion')
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
data_path = os.path.expanduser('~/pygesture-data')
# path to v-rep (needed for simulation package)
vrep_path = os.path.expanduser('~/usr/vrep/vrep-3.2.0')
# port that the v-rep is listening on (in remoteApiConnections.txt)
vrep_port = 20013

# sensor mappings
# channel_number : ('abbrv', 'muscle')
arm_sensors = {key: val[0] for (key, val) in sensors.items()}
leg_sensors = {key: val[1] for (key, val) in sensors.items()}

channels = sorted(list(arm_sensors))

probe_channel = 6

daq = daq.MccDaq(
    rate=f_samp,
    input_range=input_range,
    channel_range=(min(channels), max(channels)),
    samples_per_read=int(f_samp*(window_length-window_overlap))
)

conditioner = pipeline.Conditioner(
    order=filt_order,
    f_cut=f_cutoff,
    f_samp=f_samp,
    f_down=f_proc
)

windower = pipeline.Windower(
    length=int(f_proc*window_length),
    overlap=int(f_proc*window_overlap)
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

controller = control.Controller(vrep_actions)

results_sid_arm = ['arm1', 'arm2', 'arm3', 'arm4']
results_sid_leg = ['leg1', 'leg2', 'leg3', 'leg4']
