class Gesture(object):
    """
    Represents all data for a gesture.

    Parameters
    ----------
    label : int
        The label of the gesture, used for classification.
    name : str
        The abbreviated name. By convention, this is a two-letter string (e.g.
        "CF".
    description : str
        The expanded name. By convention, this is all lowercase, with words
        connected by hyphen (e.g. "closed-fist").
    dof : int, default=None
        The degree of freedom this gesture belongs to. Used for TAC test.
        Default is `None`, which means the gesture doesn't belong to a DOF
        (e.g. rest).
    action : str, default=None
        The action the gesture represents. The default is `None`, which means
        the gesture's action is the same as its description. This attribute can
        be useful for remapping gestures to different actions in simulation
        (e.g. let "ulnar-deviation" control "elbow-extension").
    """

    def __init__(self, label, name, description, dof=None, action=None):
        self.label = label
        self.name = name
        self.description = description
        self.dof = dof

        if action is None:
            action = description
        self.action = action


class Sensor(object):
    """
    Represents all data for a recording sensor.

    Parameters
    ----------
    channel : int
        Channel number, corresponding to the recording source (e.g. DAQ).
    name : str
        Abbreviated name of the sensor. This is usually the muscle that the
        sensor recording from (e.g. "EPL").
    description : str, default=""
        Full name of the sensor. Like the name, this typically corresponds to
        a muscle (e.g. "extensor pollicis longus").
    """

    def __init__(self, channel, name, description=""):
        self.channel = channel
        self.name = name
        self.description = description
