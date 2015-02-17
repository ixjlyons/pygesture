class PipelineBlock(object):

    def __init__(self):
        self.children = []
        self.hooks = []

    def add_child(self, node):
        self.children.append(node)

    def add_hook(self, hook):
        self.hooks.append(hook)

    def process(self, data):
        out = data  # usually some function
        self.propogate(out)

    def propogate(self, data):
        for hook in self.hooks:
            hook(data)

        for child in self.children:
            print("{0} to {1} : {2}".format(type(self), type(child), data))
            child.process(data)

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__
        )


class Recorder(PipelineBlock):

    def __init__(self, rate):
        super(Recorder, self).__init__()
        self.rate = rate

    def process(self, data):
        f = data + self.rate
        self.propogate(f)

    def __repr__(self):
        return "%s.%s(rate=%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.rate
        )


class Filter(PipelineBlock):

    def __init__(self, wc):
        super(Filter, self).__init__()
        self.wc = wc

    def process(self, data):
        out = 0
        for w in self.wc:
            out += data / float(w)

        self.propogate(out)

    def __repr__(self):
        return "%s.%s(wc=%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.wc
        )


class Filestream(PipelineBlock):

    def __init__(self, filename):
        super(Filestream, self).__init__()
        self.filename = filename

    def process(self, data):
        with open(self.filename, 'w') as f:
            f.write(str(data))

    def __repr__(self):
        return "%s.%s(filename=%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.filename
        )



