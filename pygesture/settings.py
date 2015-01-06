"""
Eventually this should be a module for loading config settings rather than
specifying them.
"""

import os

# recording settings
SAMPLE_RATE = 4096 
CHANNEL_RANGE = (0, 3)
PROBE_CHANNEL = 6
NUM_CHANNELS = CHANNEL_RANGE[1] - CHANNEL_RANGE[0] + 1
SAMPLES_PER_READ = 512 
INPUT_RANGE = 2
SECONDS_PER_RECORD = 6
TRIGGERS_PER_SECOND = int(SAMPLE_RATE / SAMPLES_PER_READ)
TRIGGERS_PER_RECORD = TRIGGERS_PER_SECOND * SECONDS_PER_RECORD
ONSET_TRANSITION = 2
OFFSET_TRANSITION = 5
INTERTRIAL_TIMEOUT = 3
DATA_ROOT = os.path.join(os.path.expanduser('~'), 'pygesture-data')
VREP_BASE_PATH = "/home/kenny/usr/v-rep/v-rep-3.1.3rev2b"

gesture_dict = {
    'l0': ('NC', 'rest'),
    'l1': ('CF', 'closed-fist'),
    'l2': ('FP', 'forearm-pronation'),
    'l3': ('FS', 'forearm-supination'),
    'l4': ('OH', 'open-hand'),
    #'l5': ('RD', 'radial-deviation'),
    #'l6': ('TE', 'thumb-extension'),
    #'l7': ('UD', 'ulnar-deviation'),
    'l5': ('WE', 'wrist-extension'),
    'l6': ('WF', 'wrist-flexion')}
#        'l10': ('EE', 'wrist-flexion-closed'),
#        'l11': ('EF', 'wrist-extension-closed') }

NUM_GESTURES = len(gesture_dict)-1
NUM_REPEATS = 3
NUM_TRIALS = NUM_GESTURES * NUM_REPEATS

arm_session_list = ['arm1', 'arm2', 'arm3', 'arm4']
leg_session_list = ['leg1', 'leg2', 'leg3', 'leg4']


arm_label_dict = {
    'l0': ('NC', 'no-contraction'),
    'l1': ('CF', 'closed-fist'),
    'l2': ('FP', 'forearm-pronation'),
    'l3': ('FS', 'forearm-supination'),
    'l4': ('OH', 'open-hand'),
    'l5': ('RD', 'radial-deviation'),
    'l6': ('TE', 'thumb-extension'),
    'l7': ('UD', 'ulnar-deviation'),
    'l8': ('WE', 'wrist-extension'),
    'l9': ('WF', 'wrist-flexion')}
#        'l10': ('EE', 'wrist-flexion-closed'),
#        'l11': ('EF', 'wrist-extension-closed') }

leg_label_dict = {
    'l0': ('NC', 'no-contraction'),
    'l1': ('TF', 'toe-flexion'),
    'l2': ('FE', 'foot-eversion'),
    'l3': ('FI', 'foot-inversion'),
    'l4': ('TE', 'toe-extension'),
    'l5': ('AD', 'foot-adduction'),
    'l6': ('HE', 'hallucis-extension'),
    'l7': ('AB', 'foot-abduction'),
    'l8': ('DF', 'dorsiflexion'),
    'l9': ('PF', 'plantarflexion')}
#        'l10': ('PFC', 'plantarflexion-closed'),
#        'l11': ('DFC', 'dorsiflexion-closed') }

arm_sensor_map = [
    ['a', 'ECR', 'extensor-carpi-radialis-brevis'],
    ['b', 'ED', 'extensor-digitorum'],
    ['c', 'EPL', 'extensor-pollicis-longus'],
    ['d', 'FDS', 'flexor-digitorum-superficialis'],
    ['e', 'FCR', 'flexor-carpi-radialis'],
    ['f', 'PT', 'pronator-teres']]

leg_sensor_map = [
    ['a', 'TA', 'tibialis-anterior'],
    ['b', 'PL', 'peroneus-longus'],
    ['c', 'GL', 'gastrocnemius-lateralis'],
    ['d', 'EHL', 'extensor-hallucis-longus'],
    ['e', 'EDL', 'extensor-digitorum-longus'],
    ['f', 'FDL', 'flexor-digitorum-longus']]


# processing settings
FC = [10, 450]
FILTER_ORDER = 4
FS_PROC = 2048
#REST_START_MS = 1000
#REST_END_MS = 1500
#GESTURE_START_MS = 2200
#GESTURE_END_MS = 4700
#WINDOW_LENGTH_MS = 100
#WINDOW_OVERLAP_MS = 0

REST_START_MS = 1000
REST_END_MS = 1500
GESTURE_START_MS = 2000
GESTURE_END_MS = 4000

SAMPS_PER_MS = int(FS_PROC / 1000)

WINDOW_OVERLAP_MS = 0
WINDOW_LENGTH_MS = int(1000 / TRIGGERS_PER_SECOND)

WINDOW_SHIFT_MS = WINDOW_LENGTH_MS - WINDOW_OVERLAP_MS

REST_START_SAMP = REST_START_MS * SAMPS_PER_MS
REST_END_SAMP = REST_END_MS * SAMPS_PER_MS
GESTURE_START_SAMP = GESTURE_START_MS * SAMPS_PER_MS
GESTURE_END_SAMP = GESTURE_END_MS * SAMPS_PER_MS
WINDOW_LENGTH_SAMP = WINDOW_LENGTH_MS * SAMPS_PER_MS
WINDOW_OVERLAP_SAMP = WINDOW_OVERLAP_MS * SAMPS_PER_MS
WINDOW_SHIFT_SAMP = WINDOW_SHIFT_MS * SAMPS_PER_MS

TRAINING_SET = ['leg1', 'leg2']
