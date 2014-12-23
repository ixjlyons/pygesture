"""
Configuration file for v-rep simulation of a robotic arm.
"""

# The port that v-rep's remote server is listening on. This is specified in
# v-rep's remoteApiConnections.txt config file
vrep_port = 20013

# Mapping from gestures to objects (joints) in the v-rep scene, with velocities
# specified in rad/s.
actions = {
    "radial-deviation": [ # aka elbow flexion
        ("IRB140_joint3", 5)
    ],
    "ulnar-deviation": [ # aka elbow extension
        ("IRB140_joint3", -5)
    ],
    "forearm-supination": [
        ("IRB140_joint4", 20)
    ],
    "forearm-pronation": [
        ("IRB140_joint4", -20)
    ],
    "wrist-extension": [
        ("IRB140_joint5", 10)
    ],
    "wrist-flexion": [
        ("IRB140_joint5", -10)
    ],
    "closed-fist": [
        ("BarrettHand_jointB_0", 10),
        ("BarrettHand_jointB_1", 10),
        ("BarrettHand_jointB_2", 10)
    ],
    "open-hand": [
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
    ],
    "thumb-extension": []
}
