# pygesture


## Description

pygesture is a collection of code for recording multi-channel EMG for the
purpose of experimenting with myoelectric gesture recognition.

Currently, a Measurement Computing USB data acquisition unit (USB-1608G) is
used for obtaining EMG data, though it should be fairly straightforward to add
support for other devices through the `daq` module.

The top-level code is primarily for handling EMG data -- filtering, feature
extraction, classification, etc. There is also a Qt GUI for recording data,
viewing and processing it, and using it for real-time gesture recogition.
Finally, there is also code for interfacing with
[v-rep](http://coppeliarobotics.com/) for robot control simulation. This is
another area which should be easy to expand
([morse](https://github.com/morse-simulator/morse) seems like a good addition
to the simulation options).


## Dependencies

The direct dependencies are all Python packages (yay!), though many of them
have non-Python dependencies. These are the direct dependencies. You will have
to find out and choose how to install them yourself. I don't know the minimum
version requirements, but I expect any Linux distro package manager to have
sufficiently up-to-date versions. Python 2 and 3 should both be supported.
I work primarily with Python 3, so if something breaks Python 2 support,
I might not notice immediately.

- [PyQt](http://www.riverbankcomputing.com/software/pyqt/intro): PyQt5 is
  required. I'd eventually like to relax this (in the style of `pyqtgraph`).
  It's not necessary if using `pygesture` as an analysis library (i.e. not
  using the `ui` subpackage at all).
- [scipy and numpy](http://www.scipy.org/): Integral to the package.
- [scikit-learn](http://scikit-learn.org/stable/): Just about as important as
  scipy and numpy.
- [pyqtgraph](http://pyqtgraph.org/): Install from the git repo to use PyQt5,
  as PyQt5 support is fairly new.

Optional:

- [pydaqflex](https://github.com/torfbolt/PyDAQFlex): Needed for use of
  a Measurement Computing DAQ.
- [PyOpenGL](http://pyopengl.sourceforge.net/): If installed, the processing
  widget in the UI takes advantage of `pyqtgraph` 3D plotting functionality, so
  clusters of points in feature space are more easily explored.
- [matplotlib](http://matplotlib.org/): The `plot_recordings` example script
  uses matplotlib.

## Versions

- v1.0 : Initial version, including real-time testing (TAC test). Used for the
  first TAC test experiment.
