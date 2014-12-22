"""
Configuration file for v-rep simulation of a robotic arm.
"""

# The port that v-rep's remote server is listening on. This is specified in
# v-rep's remoteApiConnections.txt config file
vrep_port = 20013

# Mapping from gestures to objects (joints) in the v-rep scene, with velocities
# specified in rad/s.
actions = {
    "elbow_flexion": [
        ("IRB140_joint3", 5)
    ],
    "elbow_extension": [
        ("IRB140_joint3", -5)
    ],
    "forearm_supination": [
        ("IRB140_joint4", 20)
    ],
    "forearm_pronation": [
        ("IRB140_joint4", -20)
    ],
    "wrist_extension": [
        ("IRB140_joint5", 10)
    ],
    "wrist_flexion": [
        ("IRB140_joint5", -10)
    ],
    "closed_fist": [
        ("BarrettHand_jointB_0", 10),
        ("BarrettHand_jointB_1", 10),
        ("BarrettHand_jointB_2", 10)
    ],
    "open_hand": [
        ("BarrettHand_jointB_0", -10),
        ("BarrettHand_jointB_1", -10),
        ("BarrettHand_jointB_2", -10)
    ],
    "rest": [
        ("IRB140_joint3", 0),
        ("IRB140_joint4", 0),
        ("IRB140_joint5", 0),
        ("BarrettHand_jointB_0", 0),
        ("BarrettHand_jointB_1", 0),
        ("BarrettHand_jointB_2", 0)
    ]
}
