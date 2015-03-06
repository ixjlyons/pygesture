from pygesture import control

mapping = {0 : 0, 1 : 1, 2 : 2}

class TestController(object):

    def test(self):
        data = [0]*10 + [1]*2 + [2]*5
        controller = control.Controller(mapping)

        out = []
        for l in data:
            out.append(controller.update(l))

        assert out == data


class TestLatchController(object):

    def test(self):
        data = [0]*10 + [1]*2 + [2]*5
        latch_data = [0]*14 + [2]*3

        controller = control.LatchController(
            mapping, latch_labels=[1, 2], num_required=3)

        out = []
        for l in data:
            out.append(controller.update(l))

        assert out == data


        
