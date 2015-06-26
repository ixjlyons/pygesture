from pygesture import experiment


class TestTACSession(object):

    def test_simple(self):
        gestures = {
            'ap': 0, 'am': 0,
            'bp': 1, 'bm': 1,
            'cp': 2, 'cm': 2
        }
        session = experiment.TACSession(gestures, simul=1)
        a = sorted([(g,) for g in list(gestures)])
        b = sorted(session.targets)
        assert a == b

        session = experiment.TACSession(gestures, simul=2)
        assert len(session.targets) == 12

        session = experiment.TACSession(gestures, simul=3)
        assert len(session.targets) == 8

        session = experiment.TACSession(gestures, simul=4)
        assert len(session.targets) == 0
