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

        assert out == data


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


def _run_controller(controller, data):
    out = []
    for d in data:
        out.append(controller.process(d))
    return out
