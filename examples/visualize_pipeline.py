import numpy as np
import pygraphviz as pgv

from pygesture import base
from pygesture import features

def draw_pipeline(pipeline, filename):
    """
    Renders a graph of the pipeline using pygraphviz.
    """
    G = pgv.AGraph(directed=True)
    G.node_attr['shape'] = 'box'

    G.add_node(repr(pipeline))
    _draw_children(G, pipeline)

    G.layout(prog='dot')
    G.draw(filename)

def _draw_children(G, this_node):
    # assume parent already added to graph
    for child in this_node.children:
        G.add_node(repr(child))
        G.add_edge(repr(this_node), repr(child))
        _draw_children(G, child)

def filter_hook(data):
    print("hook : {0}".format(data))


def build_pipeline():
    recorder = base.Recorder(10)
    filt = base.Filter([10, 450])
    filt.add_hook(filter_hook)
    filt2 = base.Filter([1, 10])
    filestream = base.Filestream('test.txt')
    feat = features.FeatureExtractor(
        [
            features.MAV(),
            features.WL(),
            features.ZC(thresh=0.0001),
            features.SSC(thresh=0.0001)
        ],
        6)
    
    recorder.add_child(filestream)
    recorder.add_child(filt)
    filt.add_child(filt2)
    filt2.add_child(feat)

    return recorder


if __name__ == '__main__':
    p = build_pipeline()
    p.process(np.random.rand(100, 6))
    p.process(np.random.rand(100, 6))

    draw_pipeline(p, 'test.png')
