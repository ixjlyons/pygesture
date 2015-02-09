fs = 4096
input_range = 2
trigger_rate = 8
downsample_factor = 2

data_path = '~/pygesture-data'
vrep_path = '~/usr/v-rep/v-rep-3.2.0'

# channel_number: ('abbrv', 'description')
sensors = {
    0: ('ECR', 'extensor carpi radialis brevis'),
    1: ('ED', 'extensor digitorum'),
    2: ('EPL', 'extensor pollicis longus'),
    3: ('FDS', 'flexor digitorum superficialis'),
    4: ('FCR', 'flexor carpi radialis'),
    5: ('PT', 'pronator teres')
}

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
        fc=(10, 450),
        order=4
    )
)

# 'label': ('abbrv', 'description')
gestures = {
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
