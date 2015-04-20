from pygesture import experiment


class TestTACSession(object):

    def test_simple(self):
        gestures = {
            'ap': 0, 'am': 0,
            'bp': 1, 'bm': 1,
            'cp': 2, 'cm': 2
        }
        session = experiment.TACSession(gestures, simultaneous=1)
        assert sorted(list(gestures)) == sorted(session.targets)

        session = experiment.TACSession(gestures, simultaneous=2)
        assert len(session.targets) == 12

        session = experiment.TACSession(gestures, simultaneous=3)
        assert len(session.targets) == 8

        session = experiment.TACSession(gestures, simultaneous=4)
        assert len(session.targets) == 0
