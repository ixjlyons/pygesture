import os
from pygesture import pipeline
from pygesture import features
from pygesture import processing
from pygesture import daq

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

# length of sliding window [samples]
window_length = 512
# amount of overlap between adjacent windows [samples]
window_overlap = 256

num_repeats = 3
samples_per_read = window_length - window_overlap
seconds_per_prompt = 6
gesture_time = (2, 5)
inter_trial_timeout = 3
reads_per_prompt = seconds_per_prompt * int((f_samp / samples_per_read))

# path to save/load recordings and feature CSVs
data_path = os.path.expanduser('~/pygesture-data')
# path to v-rep (needed for simulation package)
vrep_path = os.path.expanduser('~/usr/v-rep/v-rep-3.2.0')

# sensor mappings
# channel_number: ('abbrv', 'description')
arm_sensors = {
    0: ('ECR', 'extensor carpi radialis brevis'),
    1: ('ED', 'extensor digitorum'),
    2: ('EPL', 'extensor pollicis longus'),
    3: ('FDS', 'flexor digitorum superficialis'),
    4: ('FCR', 'flexor carpi radialis'),
    5: ('PT', 'pronator teres')
}
leg_sensors = {
    0: ('TA', 'tibialis anterior'),
    1: ('PL', 'peroneus longus'),
    2: ('GL', 'gastrocnemius lateralis'),
    3: ('EHL', 'extensor hallucis longus'),
    4: ('EDL', 'extensor digitorum longus'),
    5: ('FDL', 'flexor digitorum longus')
}

channels = sorted(list(arm_sensors))

probe_channel = 6

daq = daq.MccDaq(
    rate=f_samp,
    input_range=input_range, 
    channel_range=(min(channels), max(channels)),
    samples_per_read=samples_per_read
)

conditioner = pipeline.Conditioner(
    order=filt_order,
    f_cut=f_cutoff,
    f_samp=f_samp,
    f_down=f_proc
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
    feature_extractor=feature_extractor,
    rest_bounds=(int(1.0*f_proc), int(1.5*f_proc)),
    gesture_bounds=(int(2.0*f_proc), int(4.0*f_proc)),
    window_length=window_length,
    window_overlap=window_overlap
)

# gesture mappings
# 'label': ('abbrv', 'description')
arm_gestures = {
    'l0': ('NC', 'no-contraction'),
    'l1': ('CF', 'closed-fist'),
    'l2': ('FP', 'forearm-pronation'),
    'l3': ('FS', 'forearm-supination'),
    'l4': ('OH', 'open-hand'),
    'l5': ('RD', 'radial-deviation'),
    'l6': ('TE', 'thumb-extension'),
    'l7': ('UD', 'ulnar-deviation'),
    'l8': ('WE', 'wrist-extension'),
    'l9': ('UD', 'wrist-flexion')
}
leg_gestures = {
    'l0': ('NC', 'no-contraction'),
    'l1': ('TF', 'closed-fist'),
    'l2': ('FE', 'forearm-pronation'),
    'l3': ('FI', 'forearm-supination'),
    'l4': ('TE', 'open-hand'),
    'l5': ('AD', 'radial-deviation'),
    'l6': ('HE', 'thumb-extension'),
    'l7': ('AB', 'ulnar-deviation'),
    'l8': ('Df', 'wrist-extension'),
    'l9': ('PF', 'wrist-flexion')
}

results_sid_arm = ['arm1', 'arm2', 'arm3', 'arm4']
results_sid_leg = ['leg1', 'leg2', 'leg3', 'leg4']
