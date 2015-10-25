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
        ret = vrep.simxStartSimulation(
            self.clientId,
            vrep.simx_opmode_oneshot_wait)
        _validate(ret)

    def stop(self):
        """
        Stops the simulation. Can be started again.
        """
        ret = vrep.simxStopSimulation(
            self.clientId,
            vrep.simx_opmode_oneshot_wait)
        _validate(ret)

    def finish(self):
        """
        Stops the simulation and disconnects from v-rep. Starting the
        simulation after this won't work. Create a new instance to reconnect.
        """
        self.stop()
        self._disconnect()

    def _connect(self):
        vrep.simxFinish(-1)
        cid = vrep.simxStart("127.0.0.1", self.port, True, True, 1000, 5)
        if cid == -1:
            raise Exception('Failed to connect V-REP remote API server.')

        self.clientId = cid

    def _disconnect(self):
        vrep.simxFinish(self.clientId)


class Signal(object):
    """
    Generic class for convenient interfacing with signals in v-rep.

    Parameters
    ----------
    clientId : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    functions: dict
        Dictionary of remote API functions for handling the signal. Required
        keys are 'set', 'get', and 'clear'.
    """

    def __init__(self, clientId, name, functions):
        self.clientId = clientId
        self.name = name
        self.functions = functions

        self._first_read = True

    def read(self):
        """
        Reads the signal.

        Returns
        -------
        sig : relevant type for the signal (str, float, or int)
            The signal value if it has been set on the v-rep side. Returns None
            if it has not been set.
        """
        if self._first_read:
            opmode = vrep.simx_opmode_streaming
            self._first_read = False
        else:
            opmode = vrep.simx_opmode_buffer

        err, sig = self.functions['get'](
            self.clientId,
            self.name,
            opmode)

        if err == vrep.simx_return_ok:
            self._clear()
        else:
            sig = None

        return sig

    def write(self, value):
        """
        Writes a value to the signal.

        Parameters
        ----------
        value : relevant type for the signal (str, float, or int)
            Value to send to the signal.
        """
        self.functions['set'](
            self.clientId,
            self.name,
            value,
            vrep.simx_opmode_oneshot)

    def _clear(self):
        self.functions['clear'](
            self.clientId,
            self.name,
            vrep.simx_opmode_oneshot)


class StringSignal(Signal):
    """
    Class for convenient interfacing with string signals in v-rep.

    Parameters
    ----------
    clientId : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """

    def __init__(self, clientId, name):
        functions = {
            'set': vrep.simxSetStringSignal,
            'get': vrep.simxGetStringSignal,
            'clear': vrep.simxClearStringSignal
        }

        super(StringSignal, self).__init__(clientId, name, functions)


class FloatSignal(Signal):
    """
    Class for convenient interfacing with float signals in v-rep.

    Parameters
    ----------
    clientId : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """

    def __init__(self, clientId, name):
        functions = {
            'set': vrep.simxSetFloatSignal,
            'get': vrep.simxGetFloatSignal,
            'clear': vrep.simxClearFloatSignal
        }

        super(FloatSignal, self).__init__(clientId, name, functions)


class IntegerSignal(Signal):
    """
    Class for convenient interfacing with integer signals in v-rep.

    Parameters
    ----------
    clientId : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """
    def __init__(self, clientId, name):
        functions = {
            'set': vrep.simxSetIntegerSignal,
            'get': vrep.simxGetIntegerSignal,
            'clear': vrep.simxClearIntegerSignal
        }

        super(IntegerSignal, self).__init__(clientId, name, functions)


class IRB140Arm(object):
    """
    IRB140 industrial arm with optional Barrett Hand attachment. If multiple
    copies are in the scene, a suffix should be supplied. If the Barrett Hand
    attachment is used, it should have the same suffix as the parent IRB140.
    """

    joint_map = {
        'shoulder-horizontal-abduction': ('IRB140_joint2', 100),
        'shoulder-horizontal-adduction': ('IRB140_joint2', -100),
        'elbow-extension': ('IRB140_joint3', 100),
        'elbow-flexion': ('IRB140_joint3', -100),
        'forearm-supination': ('IRB140_joint4', 100),
        'forearm-pronation': ('IRB140_joint4', -100),
        'wrist-extension': ('IRB140_joint5', 100),
        'wrist-flexion': ('IRB140_joint5', -100),
        'closed-fist': ('BarrettHand', 100),
        'open-hand': ('BarrettHand', -100)
    }

    def __init__(self, clientId, suffix='', position_controlled=False,
                 lefty=False):
        self.clientId = clientId
        self.joints = None
        self.suffix = suffix
        self.position_controlled = position_controlled
        self.lefty = lefty

        self._initialize_joints()

    def _initialize_joints(self):
        res, handles, intData, floatData, names = vrep.simxGetObjectGroupData(
            self.clientId, vrep.sim_object_joint_type, 0,
            vrep.simx_opmode_oneshot_wait)

        err, self.base_handle = vrep.simxGetObjectHandle(
            self.clientId, 'IRB140'+self.suffix, vrep.simx_opmode_oneshot_wait)

        self.joints = dict()
        self.pose = dict()
        for name, handle in zip(names, handles):
            if _check_suffix(name, self.suffix):
                if 'IRB140' in name:
                    basename = name.strip(self.suffix)
                    j = Joint(
                        self.clientId,
                        name,
                        handle,
                        position_controlled=self.position_controlled)
                    self.joints[basename] = j
                    self.pose[basename] = j.initial_position

                elif 'BarrettHand_jointB_0' in name:
                    j = BarrettHand(
                        self.clientId,
                        handle,
                        suffix=self.suffix,
                        position_controlled=self.position_controlled)
                    self.joints['BarrettHand'] = j
                    self.pose['BarrettHand'] = j.initial_position

    def set_tolerance(self, tolerance):
        """
        Sets the tolerance of pose checking.

        Parameters
        ----------
        tolerance : float
            Tolerance in degrees.
        """
        vrep.simxSetFloatSignal(
            self.clientId, 'tolerance', math.radians(tolerance),
            vrep.simx_opmode_oneshot_wait)

    def set_visible(self, visible):
        """
        Sets the visibility of the robot.

        Parameters
        ----------
        visible : bool
            Model is set visible if true, invisible otherwise.
        """
        err, prop = vrep.simxGetModelProperty(
            self.clientId,
            self.base_handle,
            vrep.simx_opmode_oneshot_wait)

        if visible:
            prop &= ~vrep.sim_modelproperty_not_visible
        else:
            prop |= vrep.sim_modelproperty_not_visible

        vrep.simxSetModelProperty(
            self.clientId,
            self.base_handle,
            prop,
            vrep.simx_opmode_oneshot_wait)

    def command(self, action):
        """
        Commands the arm to perform an action. The action can be a number of
        different things.

        The simplest is a string from the `pygesture.control.CAPABILITIES`
        list. This will make the arm perform that action with a nominal
        velocity (see `IRB140Arm.joint_map`). All other actions will be turned
        off.

        Otherwise, you can specify a dictionary with action names (str) as
        keys and velocity multipliers as values. If contradictory actions (e.g.
        elbow flcodeexion and elbow extension) are specified, the velocities
        will be summed.
        """
        if type(action) is str:
            action = {action: 1}

        default_actions = dict.fromkeys(self.joint_map.keys(), 0)

        for j in self.joints.values():
            if j.position_controlled:
                j.position = j.initial_position
            else:
                j.velocity = 0

        for motion, param in action.items():
            if motion in default_actions:
                default_actions[motion] = param

        for motion, param in default_actions.items():
            joint_name, v_norm = self.joint_map[motion]
            if self.lefty and ('elbow' in motion or 'forearm' in motion):
                v_norm *= -1
            joint = self.joints[joint_name]
            if joint.position_controlled:
                sign = 1
                if v_norm < 0:
                    sign *= -1
                joint.position += sign*math.radians(param)
            else:
                joint.velocity += param*math.radians(v_norm)

        # TODO: investigate if wrapping this loop in simxPauseCommunication
        # calls would be useful here
        for name in self.joints.keys():
            self.joints[name].update()
            self.pose[name] = self.joints[name].position

    def stop(self):
        """
        Stops the robot from executing any current commands.
        """
        self.command('no-contraction')


class Joint(object):

    VELOCITY_CTRL = 0
    POSITION_CTRL = 1

    def __init__(self, clientId, name, handle, position_controlled=False):
        self.clientId = clientId
        self.name = name
        self.handle = handle
        self.velocity = 0
        self.position = 0
        self.position_controlled = position_controlled

        self.initial_position = self._get_position(
            opmode=vrep.simx_opmode_oneshot_wait)

        # set up streaming position input
        self._get_position(opmode=vrep.simx_opmode_streaming)

    def update(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        if self.position_controlled:
            res = vrep.simxSetJointTargetPosition(
                self.clientId, self.handle, self.position, opmode)
        else:
            res = vrep.simxSetJointTargetVelocity(
                self.clientId, self.handle, self.velocity, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        if not self.position_controlled:
            self.position = self._get_position(
                opmode=vrep.simx_opmode_buffer)

    def set_control_mode(self, mode):
        """
        Sets the joint mode. Either position controlled or velocity controlled
        """
        self.position_controlled = \
            True if mode == Joint.POSITION_CTRL else False
        vrep.simxSetObjectIntParameter(
            self.clientId, self.handle, 2001, mode, vrep.simx_opmode_oneshot)

    def _get_position(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        res, pos = vrep.simxGetJointPosition(
            self.clientId, self.handle, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        return pos


class MPL(object):
    """
    Modular Prosthetic Limb from Johns Hopkins Applied Physics Lab.
    """

    joint_map = {
        'shoulder-horizontal-abduction': ('mpl_shoulder_abad', -100),
        'shoulder-horizontal-adduction': ('mpl_shoulder_abad', 100),
        'elbow-extension': ('mpl_elbow', -100),
        'elbow-flexion': ('mpl_elbow', 100),
        'forearm-supination': ('mpl_forearm_prosup', 100),
        'forearm-pronation': ('mpl_forearm_prosup', -100),
        'ulnar-deviation': ('mpl_wrist_dev', -100),
        'radial-deviation': ('mpl_wrist_dev', 100),
        'wrist-extension': ('mpl_wrist_extflex', -100),
        'wrist-flexion': ('mpl_wrist_extflex', 100),
        'closed-fist': ('mpl_index1_joint', 100),
        'open-hand': ('mpl_index1_joint', -100)
    }

    def __init__(self, clientId, suffix='', position_controlled=True):
        self.clientId = clientId
        self.joints = None
        self.suffix = suffix
        self._position_controlled = position_controlled

        self._initialize_joints()

    def _initialize_joints(self):
        res, handles, intData, floatData, names = vrep.simxGetObjectGroupData(
            self.clientId, vrep.sim_object_joint_type, 0,
            vrep.simx_opmode_oneshot_wait)

        err, self.base_handle = vrep.simxGetObjectHandle(
            self.clientId, 'mpl'+self.suffix, vrep.simx_opmode_oneshot_wait)

        self.joints = dict()
        self.pose = dict()
        controlled_joints = [t[0]+self.suffix for t in MPL.joint_map.values()]
        for name, handle in zip(names, handles):
            if name in controlled_joints:
                basename = name.strip(self.suffix)
                j = Joint(
                    self.clientId,
                    name,
                    handle,
                    position_controlled=self._position_controlled)
                self.joints[basename] = j
                self.pose[basename] = j.initial_position

    @property
    def position_controlled(self):
        return self._position_controlled

    @position_controlled.setter
    def position_controlled(self, value):
        self._position_controlled = value
        mode = Joint.POSITION_CTRL if value else Joint.VELOCITY_CTRL
        for j in self.joints.values():
            j.set_control_mode(mode)

    def set_visible(self, visible):
        """
        Sets the visibility of the robot.

        Parameters
        ----------
        visible : bool
            Model is set visible if true, invisible otherwise.
        """
        err, prop = vrep.simxGetModelProperty(
            self.clientId,
            self.base_handle,
            vrep.simx_opmode_oneshot_wait)

        if visible:
            prop &= ~vrep.sim_modelproperty_not_visible
        else:
            prop |= vrep.sim_modelproperty_not_visible

        vrep.simxSetModelProperty(
            self.clientId,
            self.base_handle,
            prop,
            vrep.simx_opmode_oneshot_wait)

    def command(self, action):
        """
        Commands the arm to perform an action. The action can be a number of
        different things.

        The simplest is a string from the `pygesture.control.CAPABILITIES`
        list. This will make the arm perform that action with a nominal
        velocity (see `IRB140Arm.joint_map`). All other actions will be turned
        off.

        Otherwise, you can specify a dictionary with action names (str) as
        keys and velocity multipliers as values. If contradictory actions (e.g.
        elbow flexion and elbow extension) are specified, the velocities will
        be summed.
        """
        if type(action) is str:
            action = {action: 1}

        default_actions = dict.fromkeys(self.joint_map.keys(), 0)

        for j in self.joints.values():
            if j.position_controlled:
                j.position = j.initial_position
            else:
                j.velocity = 0

        for motion, param in action.items():
            if motion in default_actions:
                default_actions[motion] = param

        for motion, param in default_actions.items():
            joint_name, v_norm = self.joint_map[motion]
            joint = self.joints[joint_name]
            if joint.position_controlled:
                sign = 1
                if v_norm < 0:
                    sign *= -1
                joint.position += sign*math.radians(param)
            else:
                joint.velocity += param*math.radians(v_norm)

        # TODO: investigate if wrapping this loop in simxPauseCommunication
        # calls would be useful here
        for name in self.joints.keys():
            self.joints[name].update()
            self.pose[name] = self.joints[name].position

    def stop(self):
        """
        Stops the robot from executing any current commands.
        """
        self.command('no-contraction')


class BarrettHand(object):

    def __init__(self, clientId, handle, suffix='', position_controlled=False):
        # handle is needed for at least one MCP joint (jointB) to get position
        self.clientId = clientId
        self.name = 'BarrettHand'+suffix
        self.handle = handle
        self.suffix = suffix
        self.position_controlled = position_controlled
        self.velocity = 0
        self.position = 0

        self.initial_position = self._get_position(
            opmode=vrep.simx_opmode_oneshot_wait)

        if position_controlled:
            append = '_position'
        else:
            self._get_position(opmode=vrep.simx_opmode_streaming)
            append = '_velocity'
        self.signal_name = 'BarrettHand' + self.suffix + append

    def update(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        if self.position_controlled:
            param = self.position
        else:
            param = self.velocity

        res = vrep.simxSetFloatSignal(
            self.clientId, self.signal_name, param, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        if not self.position_controlled:
            self.position = self._get_position(
                opmode=vrep.simx_opmode_buffer)

    def _get_position(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        res, pos = vrep.simxGetJointPosition(
            self.clientId, self.handle, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        return pos


def _validate(res):
    if res != vrep.simx_return_ok:
        err = ""
        if res == vrep.simx_return_novalue_flag:
            err = "Input buffer doesn't contain the specified command"
        elif res == vrep.simx_return_timeout_flag:
            err = "Command reply not received in time for wait opmode"
        elif res == vrep.simx_return_illegal_opmode_flag:
            err = "Command odesn't support specified opmode"
        elif res == vrep.simx_return_remote_error_flag:
            err = "Command caused an error on the server side"
        elif res == vrep.simx_return_split_progress_flag:
            err = "Previous similar command not processed yet"
        elif res == vrep.simx_return_local_error_flag:
            err = "Command caused an error on the client side"
        elif res == vrep.simx_return_initialize_error_flag:
            err = "simxStart not yet called"
        else:
            err = "Unknown v-rep error code: %s" % hex(res)

        raise ValueError(err)


def _check_suffix(name, suffix):
    if suffix == '':
        if len(name.split('#')) == 1:
            return True
        else:
            return False
    else:
        if suffix in name:
            return True
        else:
            return False
