from pygesture import pipeline

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

# path to save/load recordings and feature CSVs
data_path = '~/pygesture-data'
# path to v-rep (needed for simulation package)
vrep_path = '~/usr/v-rep/v-rep-3.2.0'

recorder = dict( 
    fs=fs,
    channels=list(sensors.keys()),
    trigger_rate=trigger_rate,
    input_range=input_range
)

processor = dict(
    input_fs=fs,
    downsample_factor=2,
    bandpass_filter=dict(
        fs=f_samp,
        order=4,
        fc=(10, 450)
    )
    )
)

conditioner = pipeline.Conditioner(
    order=4,
    f_cut=(8, 512),
    f_samp=f_samp,
    f_down=k)

# sensor mappings
# channel_number: ('abbrv', 'description')
sensors_arm = {
    0: ('ECR', 'extensor carpi radialis brevis'),
    1: ('ED', 'extensor digitorum'),
    2: ('EPL', 'extensor pollicis longus'),
    3: ('FDS', 'flexor digitorum superficialis'),
    4: ('FCR', 'flexor carpi radialis'),
    5: ('PT', 'pronator teres')
}
sensors_leg = {
    0: ('TA', 'tibialis anterior'),
    1: ('PL', 'peroneus longus'),
    2: ('GL', 'gastrocnemius lateralis'),
    3: ('EHL', 'extensor hallucis longus'),
    4: ('EDL', 'extensor digitorum longus'),
    5: ('FDL', 'flexor digitorum longus')
}

# gesture mappings
# 'label': ('abbrv', 'description')
gestures_arm = {
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
gestures_leg = {
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
