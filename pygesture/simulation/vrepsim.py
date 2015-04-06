import math
import os
import platform
import importlib

vrep = None


def set_path(path):
    """
    Sets an environment variable for loading v-rep's remote API dynamic linked
    library. Right now it will only work on Linux but it is kind of a hack
    anyway. A better approach is needed, but the Python bindings v-rep provides
    make it not very straightforward without modification. This must be done
    before using the rest of this module, making it even more evil.
    """
    global vrep
    remote_path = os.path.join(
        path, "programming", "remoteApiBindings", "lib", "lib")

    if platform.architecture()[0] == '64bit':
        remote_lib = os.path.join(remote_path, "64Bit", "remoteApi.so")
    else:
        remote_lib = os.path.join(remote_path, "32Bit", "remoteApi.so")

    os.environ['VREPLIB'] = remote_lib

    vrep = importlib.import_module('pygesture.simulation.vrep')


class VrepSimulation(object):

    def __init__(self, port=19997):
        """
        Initializes a connection to v-rep. The v-rep program should already be
        running and it should be configured to run in continuous remote API
        mode.
        """
        self.clientId = -1
        self.port = port
        self._connect()

    def start(self):
        """
        Starts the simulation. Use stop() to stop the simulation or finish() to
        stop and kill the connection to the v-rep server.
        """
        vrep.simxStartSimulation(self.clientId, vrep.simx_opmode_oneshot_wait)

    def stop(self):
        """
        Stops the simulation. Can be started again.
        """
        vrep.simxStopSimulation(self.clientId, vrep.simx_opmode_oneshot_wait)

    def finish(self):
        """
        Stops the simulation and disconnects from v-rep. Starting the
        simulation after this won't work. Create a new instance to reconnect.
        """
        self.stop()
        self._disconnect()

    def _connect(self):
        vrep.simxFinish(-1)
        cid = vrep.simxStart("127.0.0.1", self.port, True, True, 5000, 5)
        if cid == -1:
            raise Exception('Failed to connect V-REP remote API server.')

        self.clientId = cid

    def _disconnect(self):
        vrep.simxFinish(self.clientId)


class IRB140Arm(object):
    """
    IRB140 industrial arm with Barrett Hand attachment.
    """

    joint_map = {
        'shoulder-horizontal-abduction': ('IRB140_joint2', 5),
        'shoulder-horizontal-adduction': ('IRB140_joint2', -5),
        'elbow-extension': ('IRB140_joint3', 5),
        'elbow-flexion': ('IRB140_joint3', -5),
        'forearm-supination': ('IRB140_joint4', 20),
        'forearm-pronation': ('IRB140_joint4', -20),
        'wrist-extension': ('IRB140_joint5', 10),
        'wrist-flexion': ('IRB140_joint5', -10),
        'closed-fist': ('BarrettHand', 60),
        'open-hand': ('BarrettHand', -60)
    }

    def __init__(self, clientId):
        self.clientId = clientId
        self.joints = None

        self._initialize_joints()

    def _initialize_joints(self):
        res, handles, intData, floatData, names = vrep.simxGetObjectGroupData(
            self.clientId, vrep.sim_object_joint_type, 0,
            vrep.simx_opmode_oneshot_wait)

        self.joints = dict()
        hand_attached = False
        for name, handle in zip(names, handles):
            if 'IRB140' in name:
                joint = Joint(self.clientId, name, handle)
                self.joints[name] = joint
            elif 'BarrettHand' in name:
                hand_attached = True

        if hand_attached:
            self.joints['BarrettHand'] = BarrettHand(self.clientId)

    def command(self, action):
        """
        Commands the arm to perform an action. The action can be a number of
        different things.

        The simplest is a string from the `pygesture.control.CAPABILITIES`
        list. This will make the arm perform that action with a nominal
        velocity (see `IRB140Arm.joint_map`). All other actions will be turned
        off.

        Ohterwise, you can specify a dictionary with action names (str) as
        keys and velocity multipliers as values. If contradictory actions (e.g.
        elbow flexion and elbow extension) are specified, the velocities will
        be summed.
        """
        if type(action) is str:
            action = {action: 1}

        default_actions = dict.fromkeys(IRB140Arm.joint_map.keys(), 0)

        for j in self.joints.values():
            j.velocity = 0

        for motion, v_mult in action.items():
            if motion in default_actions:
                default_actions[motion] = v_mult

        for motion, v_mult in default_actions.items():
            joint_name, v_norm = self.joint_map[motion]
            self.joints[joint_name].velocity += v_mult*math.radians(v_norm)

        # TODO: investigate if wrapping this loop in simxPauseCommunication
        # calls would be useful here
        for j in self.joints.values():
            j.update()

    def stop(self):
        """
        Stops the robot from executing any current commands.
        """
        self.command('no-contraction')


class Joint(object):

    def __init__(self, clientId, name, handle):
        self.clientId = clientId
        self.name = name
        self.handle = handle
        self.velocity = 0

    def update(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        res = vrep.simxSetJointTargetVelocity(
            self.clientId, self.handle, self.velocity, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)


class BarrettHand(object):

    def __init__(self, clientId):
        self.clientId = clientId
        self.name = 'BarrettHand'
        self.velocity = 0

    def update(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        res = vrep.simxSetFloatSignal(
            self.clientId, 'velocity', self.velocity, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)


def _validate(res):
    if res != vrep.simx_error_noerror:
        err = ""
        if res == vrep.simx_error_novalue_flag:
            err = "Input buffer doesn't contain the specified command"
        elif res == vrep.simx_error_timeout_flag:
            err = "Command reply not received in time for wait opmode"
        elif res == vrep.simx_error_illegal_opmode_flag:
            err = "Command odesn't support specified opmode"
        elif res == vrep.simx_error_remote_error_flag:
            err = "Command caused an error on the server side"
        elif res == vrep.simx_error_split_progress_flag:
            err = "Previous similar command not processed yet"
        elif res == vrep.simx_local_error_flag:
            err = "Command caused an error on the client side"
        elif res == vrep.simx_error_initialize_error_flag:
            err = "simxStart not yet called"
        else:
            err = "Unknown v-rep error code: %s" % hex(res)

        raise ValueError(err)
