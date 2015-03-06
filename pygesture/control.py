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

class Controller(object):
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

    def update(self, label):
        return self.mapping[label]


class LatchController(object):
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
        Deafult is 1, meaning no latching.
    """

    def __init__(self, mapping, latch_labels=[], num_required=1):
        self.mapping = mapping
        self.latch_labels = latch_labels
        self.history = [0]*num_required

    def update(self, label):
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
            self.history = self.history[1:]
        else:
            self.history = [label]

    def _check_latch(self, label):
        for h in self.history:
            if h != label:
                return False
        return True


class DBVRController(object):
    """
    Decision-based velocity ramp controller (see [1]).

    Parameters
    ----------
    mapping : dict {int: Action}
        Mapping from gesture class label to prosthetic action.
    majority_vote : int, default=0
        Number of past examples to include in majority vote. Default is zero,
        meaning no majority vote is taken and the current label is used
        directly.

    References
    ----------
    .. [1] `A. M. Simon, L. J. Hargrove, B. A. Lock, and T. A. Kuiken, "A
        Decision-Based Velocity Ramp for Minimizing the Effect of
        Misclassifications During Real-Time Pattern Recognition Control," IEEE
        Transactions on Biomedical Engineering, vol. 58, no. 8, 2011.
    """

    def __init__(self, mapping, ramp_length, majority_vote=0):
        pass

    def update(self, label, speed):
        pass
