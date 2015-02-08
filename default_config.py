import os

data_path = os.path.join(
    os.path.expanduser('~'), 'pygesture-data')
vrep_path = os.path.join(
    os.path.expanduser('~'), 'usr', 'v-rep', 'v-rep-3.2.0')

# these classes are templates which will go in a config module
class Sensor:
    def __init__(self, channel, label='', name=''):
        self.channel = channel
        self.label = label
        self.name = name

class Gesture:
    def __init__(self, label, abbrv='', name=''):
        self.label = label
        self.name = name
        self.abbrv = abbrv

sensors = [
    Sensor(0, 'ECR', 'extensor carpi radialis brevis'),
    Sensor(1, 'ED', 'extensor digitorum'),
    Sensor(2, 'EPL', 'extensor pollicis longus'),
    Sensor(3, 'FDS', 'flexor digitorum superficialis'),
    Sensor(4, 'FCR', 'flexor carpi radialis'),
    Sensor(5, 'PT', 'pronator teres')
]

# local variables not picked up by config
fs = 4096
downsample_factor = 2

recorder = Recorder(
    fs=fs,
    channels=channels 
    )

processor = Processor(
        input_fs=fs,
        conditioning=[
            BandpassFilter((10, 450), 4),
            Downsampler(downsample_factor)
        ]
    )


# Gesture(label, description)
gestures = [
    Gesture('l0', 'NC', 'no-contraction'),
    Gesture('l1', 'CF', 'closed-fist'),
    Gesture('l2', 'FP', 'forearm-pronation'),
    Gesture('l3', 'FS', 'forearm-supination'),
    Gesture('l4', 'OH', 'open-hand'),
    Gesture('l5', 'RD', 'radial-deviation'),
    Gesture('l6', 'TE', 'thumb-extension'),
    Gesture('l7', 'UD', 'ulnar-deviation'),
    Gesture('l8', 'WE', 'wrist-extension'),
    Gesture('l9', 'UD', 'wrist-flexion')
]

