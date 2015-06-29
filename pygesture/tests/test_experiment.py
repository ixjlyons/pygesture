from pygesture import experiment
from pygesture import util


class TestTACSession(object):

    def test_simple(self):
        gestures = [
            util.Gesture(0, "0a", "", dof=0),
            util.Gesture(1, "0b", "", dof=0),
            util.Gesture(2, "1a", "", dof=1),
            util.Gesture(3, "1b", "", dof=1),
            util.Gesture(4, "2a", "", dof=2),
            util.Gesture(5, "2b", "", dof=2)
        ]

        session = experiment.TACSession(gestures, simul=1)
        a = sorted(gestures, key=lambda g: g.label)
        b = sorted([t[0] for t in session.targets], key=lambda g: g.label)
        assert a == b

        session = experiment.TACSession(gestures, simul=2)
        assert len(session.targets) == 12

        session = experiment.TACSession(gestures, simul=3)
        assert len(session.targets) == 8

        session = experiment.TACSession(gestures, simul=4)
        assert len(session.targets) == 0
