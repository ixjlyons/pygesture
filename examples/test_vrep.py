#!/usr/bin/env python

"""
This script tests pygesture's coordination with the v-rep robotic simulation
environment. Before running, ensure the following are in place:
    * v-rep is running and has a remote API server running on the default port
      (19997).
    * The `mpl_tac_test.ttt` scene in the repo's `vrep_scenes` dir is loaded.

Specifically, the tests include:
    * Putting the arm in position control mode, commanding it to a variety of
      postures, and asserting that the actual posture matches the commanded
      one.
    * Putting the arm in an off-target posture, putting the arm in velocity
      control mode, commanding it back to the netural posture, and checking
      the `target_acquired` signal (embedded script in the scene).

Note that the velocity control test will only work in real-time simulation
mode.
"""

import sys
import argparse
import time
import math
import copy

from numpy.testing import assert_approx_equal

try:
    from pygesture import config
except ImportError:
    sys.path.insert(0, '..')
    from pygesture import config

from pygesture import control
from pygesture.simulation import vrepsim


rest_time = 0.75

position_commands = [
    {
        'command': 'elbow-extension',
        'angle': 20,
        'joint': 'mpl_elbow'
    },
    {
        'command': 'closed-fist',
        'angle': 30,
        'joint': 'mpl_index1_joint'
    },
    {
        'command': 'forearm-pronation',
        'angle': 50,
        'joint': 'mpl_forearm_prosup'
    },
    {
        'command': 'wrist-extension',
        'angle': 15.2,
        'joint': 'mpl_wrist_extflex'
    }
]

def main(args):
    cfg = config.Config(args.config)

    sim = vrepsim.VrepSimulation()
    sim.start()

    arm = vrepsim.MPL(sim.clientId)
    init_pose = copy.deepcopy(arm.pose)

    time.sleep(1)

    #
    # test position control
    #

    arm.position_controlled = True
    for cmd in position_commands:
        # move a joint to a specific position
        arm.command({cmd['command']: cmd['angle']})

        # calculate the angle actually travelled by the joint
        d = diff(init_pose, arm.pose, cmd['joint'])
        # ensure the target angle and the actual angle are equal
        assert_approx_equal(cmd['angle'], d)

        time.sleep(rest_time)

    #
    # test velocity control
    #

    # put the arm in the target posture
    arm.command('no-contraction')
    time.sleep(rest_time)

    # signal should be 0 when the arm leaves the target and 1 when it enters
    acqsig = vrepsim.IntegerSignal(sim.clientId, 'target_acquired')
    acq = acqsig.read()

    # put the arm in an out-of-target posture
    arm.command({'wrist-flexion': 50})
    time.sleep(rest_time)

    # arm should have started in the target posture and exited it during the
    # previous command
    acq = acqsig.read()
    assert acq == 0

    # turn off position control (velocity control)
    arm.position_controlled = False
    # get the max wrist extension rate (deg/s)
    max_we = abs(vrepsim.MPL.joint_map['wrist-extension'][1])
    # command the arm to extend the wrist (counter-act the previous
    # wrist-flexion command)
    arm.command({'wrist-extension': 0.5})
    # wait until the arm reaches the neutral posture again
    time.sleep(50 / (0.5*max_we))
    arm.command('no-contraction')

    # arm should now be in the neutral posture
    acq = acqsig.read()
    assert acq == 1

    time.sleep(1)

    sim.finish()


def diff(init, current, name):
    return abs(math.degrees(init[name] - current[name]))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Runs through a pre-programmed sequence of movements.")
    parser.add_argument('-c', '--config', default='config.py',
        help="Config file. Default is `config.py` (current directory).")

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
