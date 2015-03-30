import numpy as np

from pygesture import pipeline

# standard set of capabilities
CAPABILITIES = [
    'no-contraction',
    'elbow-flexion'
    'elbow-extension',
    'forearm-pronation',
    'forearm-supination',
    'wrist-flexion',
    'wrist-extension',
    'open-hand',
    'closed-fist'
]


class Controller(pipeline.PipelineBlock):
    """
    Takes gesture class predictions and outputs commands to the simulation.
    This base implementation simply passes through the action corresponding to
    the input gesture label.

    Parameters
    -----------
    mapping : dict {int : Action}
        Mapping from gesture class label to prosthetic action.
    """

    def __init__(self, mapping):
        self.mapping = mapping

    def process(self, label):
        return self.mapping[label]


class LatchController(Controller):
    """
    Simple controller that puts elbow/forearm/wrist straight through, but
    requires that hand open/close commands "latch", meaning a certain number of
    consecutive inputs need to be input before opening/closing the hand fully.

    Parameters
    ----------
    mapping : dict {int : Action}
        Mapping from gesture class label to prosthetic action.
    latch_labels : list, default=[]
        List of labels which should be latched. Default is empty, meaning no
        latching occurs.
    num_required : int, default=1
        Number of consecutive instances of a label for it to be latched.
        Default is 1, meaning no latching.
    """

    def __init__(self, mapping, latch_labels=[], num_required=1):
        super(LatchController, self).__init__(mapping)
        self.latch_labels = latch_labels
        self.history = [0] * num_required

    def process(self, label):
        self._update_history(label)

        if label in self.latch_labels:
            if self._check_latch(label):
                out_label = label
            else:
                out_label = 0
        else:
            out_label = label

        return self.mapping[out_label]

    def _update_history(self, label):
        if len(self.history) > 1:
            self.history = self.history[1:] + [label]
        else:
            self.history = [label]

    def _check_latch(self, label):
        for h in self.history:
            if h != label:
                return False
        return True


class DBVRController(Controller):
    """
    Decision-based velocity ramp controller (see [1]).

    The controller takes two inputs (MAV of each channel, class label) and
    outputs a single label. A Pipeline construction should take this into
    account.

    Parameters
    ----------
    mapping : dict {int: Action}
        Mapping from gesture class label to prosthetic action.
    ramp_length : int
        Length of the ramp -- the number of consecutive inputs of the same
        class label before full velocity is achieved.
    boosts : float or dict
        Boost value for each class (e.g. {0: 0.2, 1: 0.5,...}) or a single
        value (boosts equal for all classes). Default is 1.

    References
    ----------
    .. [1] `A. M. Simon, L. J. Hargrove, B. A. Lock, and T. A. Kuiken, "A
        Decision-Based Velocity Ramp for Minimizing the Effect of
        Misclassifications During Real-Time Pattern Recognition Control," IEEE
        Transactions on Biomedical Engineering, vol. 58, no. 8, 2011.
    """

    def __init__(self, mapping, ramp_length=10, boosts=1):
        super(DBVRController, self).__init__(mapping)
        self.ramp_length = ramp_length

        if type(boosts) == dict:
            self.boosts = boosts
        else:
            self.boosts = dict.fromkeys(mapping.keys(), boosts)

        self.restless_mapping = {}
        for key, val in mapping.items():
            if val != 'no-contraction':
                self.restless_mapping[key] = val

        self._reset_values()

    def _reset_values(self):
        k = self.restless_mapping.keys()
        self._counts = dict.fromkeys(k, 0)
        self._gains = dict.fromkeys(k, 0)
        self._vin = dict.fromkeys(k, 0)
        self._vout = {self.mapping[key]: 0 for key in self.restless_mapping}

    def process(self, data):
        mav, label = data

        if self.mapping[label] == 'no-contraction':
            self._reset_values()
            return 'no-contraction'

        self._update_gains(label)

        mav_avg = np.mean(mav)

        for i in self._vin:
            self._vin[i] = self.boosts[i] * mav_avg
            self._vout[self.mapping[i]] = self._gains[i] * self._vin[i]

        return self._vout.copy()

    def _update_gains(self, label):
        for l in self._counts:
            if l == label:
                self._counts[l] += 1
            else:
                self._counts[l] -= 2

            if self._counts[l] > self.ramp_length:
                self._counts[l] = self.ramp_length

            if self._counts[l] < 0:
                self._counts[l] = 0

            self._gains[l] = self._counts[l] / float(self.ramp_length)
