# pygesture

[![DOI](https://zenodo.org/badge/44645368.svg)](https://zenodo.org/badge/latestdoi/44645368)

## Description

pygesture is a collection of code for recording multi-channel EMG for the
purpose of experimenting with myoelectric gesture recognition.

Several signal input sources are supported:

* Delsys Trigno wireless EMG system, via TCP connection to the Trigno Control
  Utility.

* Measurement Computing USB data acquisition unit(s). Right now, only the
  USB-1608G is implemented/tested, but additional MCC DAQs can be easily
  supported (thanks to pyusb and pydaqflex).

The top-level code is primarily for handling EMG data -- filtering, feature
extraction, classification, etc. There is also a Qt GUI for recording data,
viewing and processing it, and using it for real-time gesture recogition.
Finally, there is also code for interfacing with
[v-rep](http://coppeliarobotics.com/) for robot control simulation. This is an
area that I would like to expand on a bit.
[morse](https://github.com/morse-simulator/morse) seems like a good candidate
for addition to the simulation options.


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


## Development

The recommended approach is to set up a virtual environment with system site
packages (because the dependencies don't pip install nicely) and install in
develop mode:

```
virtualenv --system-site-packages env
source env/bin/activate
python setup.py develop
```

Now you should be able to run the main GUI by just running `pygesture`.

The test coverage is pretty terrible, but you can run tests anyway:

```
python setup.py test
```

Note that it isn't really feasible to test everything `pygesture` does with
unit tests, such as data acquisition and simulation, since they assume you have
additional software running or hardware connected. For these things, there are
test scripts in the `examples/` directory. These "test-like" scripts are all
named `test_*.py`. Specific instructions for running them are included in the
scripts themselves.

You can also run static code checks (requires
[flake8](https://gitlab.com/pycqa/flake8)):

```
make lint
```


## Setting up v-rep

To get v-rep working, you need to set an environment variable `VREP` with the
full path to v-rep's installed location. On Linux, this is wherever you extract
the tarball v-rep distributes. You might want to put an appropriate entry in
your bashrc, for example: `export VREP='~/usr/vrep/vrep-3.2.2'`. On Windows, it
installs to somewhere like `C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU`. Find
this location (you should see lots of dlls) and add a `VREP` system environment
variable.

You can test communication with v-rep by loading up the
`vrep_scenes/mpl_tac_test.ttt` scene and running `examples/test_vrep.py`. If
that script runs smoothly, everything should be set up correctly. It also
provides some example usage of the `vrepsim` module.


## Setting up the Measurement Computing USB DAQ

The Measurement Computing (MCC) DAQ relies on the
[DAQFlex](http://www.mccdaq.com/daq-software/DAQFlex.aspx) library and
[pydaqflex](https://github.com/torfbolt/PyDAQFlex). Start by installing DAQFlex
on your chosen platform. On Windows, that *should* be all that's needed. On
Linux, you'll need to install the udev rule file (`tools/60-mcc.rules`). Once
that's done, install pydaqflex. Finally, try running the
`examples/test_mccdaq.py` script. If no errors occur, the device should be set
up correctly.


## Setting up the Delsys Trigno wireless EMG system

The Trigno system only has USB drivers for Windows, and interfacing with the
device goes through the Trigno Control Utility. It is essentially a program
that runs a TCP server to which you can connect to control the device and
retrieve data. To use the Trigno system, start up Trigno Control Utility
before running pygesture or some other script. Try running
`examples/test_trigno.py` to see if things are set up correctly -- if no errors
occur, it should be ready to go.


## Versions

- v1.0 : Initial version, including real-time testing (TAC test). Used for the
  first TAC test experiment.
- v2.0 : Second version, used for the second TAC test experiment published in
  IEEE Transactions on Neural Systems and Rehabilitation Engineering.
