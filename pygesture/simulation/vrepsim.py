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

    system = platform.system()
    if platform.architecture()[0] == '64bit':
        remote_lib = os.path.join(remote_path, "64Bit", "remoteApi.so")
    else:
        remote_lib = os.path.join(remote_path, "32Bit", "remoteApi.so")

    os.environ['VREPLIB'] = remote_lib

    vrep = importlib.import_module('pygesture.simulation.vrep')


class VrepSimulation:

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


class Robot:

    def __init__(self, clientId, actions):
        self.clientId = clientId
        self.actions = actions
        self.joints = None

        self.initialize_joints()

    def initialize_joints(self, query=""):
        objectType = vrep.sim_object_joint_type
        res, handles, intData, floatData, names = vrep.simxGetObjectGroupData(
            self.clientId, objectType, 0, vrep.simx_opmode_oneshot_wait)
        #validate(res)
        joints = dict()
        for i in range(len(names)): 
            if query not in names[i]:
                continue
            joint = Joint(self.clientId, names[i], handles[i])
            joint.initialize()
            joints[names[i]] = joint
        
        self.joints = joints

    def do_action(self, action_name):
        action = self.actions[action_name]

        if action_name == 'closed-fist':
            res = vrep.simxSetIntegerSignal(self.clientId, 'request', 1, vrep.simx_opmode_oneshot)
        elif action_name == 'open-hand':
            res = vrep.simxSetIntegerSignal(self.clientId, 'request', 2, vrep.simx_opmode_oneshot)
        else:
            # TODO pause comm, send all commands, then resume comm
            if action_name == 'rest':
                res = vrep.simxSetIntegerSignal(self.clientId, 'request', 0, vrep.simx_opmode_oneshot)

            for joint_name, vel_deg in action:
                j = self.joints[joint_name]
                vel_rad = math.radians(vel_deg)
                vrep.simxSetJointTargetVelocity(self.clientId, j.handle, vel_rad,
                    vrep.simx_opmode_oneshot)


class Joint(object):

    def __init__(self, clientId, name, handle):
        self.clientId = clientId
        self.name = name
        self.handle = handle
        self.position = None
        self.force = None

    def __repr__(self):
        return "(name={0}, handle={1}, position={2:2.5f}, force={3:.5f})".format(
            self.name, self.handle, self.position, self.force)

    def initialize(self):
        self.getPosition()
        self.getForce()

    def getPosition(self):
        res, self.position = vrep.simxGetJointPosition(self.clientId,
            self.handle, vrep.simx_opmode_oneshot_wait)
        validate(res)

    def setPosition(self, position):
        res = vrep.simxSetJointPosition(self.clientId, self.handle, position,
            vrep.simx_opmode_oneshot)
        validate(res)
        self.getPosition()

    def getForce(self):
        res, self.force = vrep.simxGetJointForce(self.clientId, self.handle,
            vrep.simx_opmode_oneshot_wait)
        validate(res)

    def setForce(self, force):
        res = vrep.simxSetJointForce(self.clientId, self.handle, force,
            vrep.simx_opmode_oneshot)
        validate(res)
        self.getForce()


def validate(res):
    if res != vrep.simx_error_noerror:
        raise ValueError("Error code returned")
