from pygesture import control


class TestController(object):

    def test(self):
        mapping = {0: 0, 1: 1, 2: 2}
        data = [0]*10 + [1]*2 + [2]*5
        controller = control.Controller(mapping)

        out = _run_controller(controller, data)

        assert out == data


class TestLatchController(object):

    def test(self):
        mapping = {0: 0, 1: 1, 2: 2}
        data = [0]*10 + [1]*2 + [2]*5
        latch_data = [0]*14 + [2]*3

        controller = control.LatchController(
            mapping, latch_labels=[1, 2], num_required=3)

        out = _run_controller(controller, data)

        assert out == latch_data


class TestDBVRController(object):

    def test_simple(self):
        mapping = {0: 0, 1: 1, 2: 2}
        labels = [0]*10
        mav = [1]*len(labels)
        data = zip(mav, labels)

        controller = control.DBVRController(
            mapping, ramp_length=5, boosts=1)

        out = _run_controller(controller, data)

        on_ramp = out[3][0]
        saturated = out[5][0]

        assert on_ramp > 0 and on_ramp < 1
        assert saturated == 1

    def test_complex(self):
        mapping = {0: 'no-contraction', 1: '1', 2: '2'}

        controller = control.DBVRController(
            mapping, ramp_length=5, boosts=1)

        out = controller.process((1, 0))
        assert out == 'no-contraction'
        out = controller.process((1, 1))
        assert out['1'] > 0
        assert out['2'] == 0
        out = controller.process((1, 2))
        assert out['1'] == 0
        assert out['2'] > 0

    def test_ramp_length_1(self):
        mapping = {0: '0', 1: '1'}

        controller = control.DBVRController(
            mapping, ramp_length=1, boosts=1)

        out = controller.process((1, 0))
        assert out == {'0': 1, '1': 0}
        out = controller.process((1, 1))
        assert out == {'0': 0, '1': 1}

    def test_boosts(self):
        mapping = {0: '0', 1: '1'}
        boosts = {0: 2, 1: 1}
        labels = [0]*7 + [1]*7
        mav = [1]*len(labels)
        data = zip(mav, labels)

        controller = control.DBVRController(
            mapping, ramp_length=5, boosts=boosts)

        out = _run_controller(controller, data)
        assert out[5]['0'] == 1
        assert out[-1]['1'] == 1

    def test_mav(self):
        mapping = {0: '0', 1: '1'}

        controller = control.DBVRController(
            mapping, ramp_length=1, boosts=1)

        out = controller.process((0.8, 0))
        assert out == {'0': 0.8, '1': 0}


def _run_controller(controller, data):
    out = []
    for d in data:
        out.append(controller.process(d))
    return out
