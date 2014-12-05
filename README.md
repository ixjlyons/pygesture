# pygesture

## Description

pygesture is a collection of code for recording multi-channel EMG for the
purpose of experimenting with myoelectric gesture recognition.

Currently, a Measurement Computing USB data acquisition unit (USB-1608G) is
used for obtaining EMG data, though it should be fairly straightforward to use
other devices if needed.

There are basically two types of code here: Qt GUIs for recording data and/or
playing with real-time gesture recogition and processing code for offline
analysis. Eventually, I'd like the same data processing code to be used for
both, but it's not quite there yet.

### GUI program: pygesture

This is "the original" pygesture. It is for prompting the user for a randomly
selected gesture, recording data for a set amount of time, then writing this
data directly to disk. That's it.

### GUI program: pygesture-rt

This is an in-development effort for testing real-time gesture recognition with
a simple feedback interface.

## Dependencies

The direct dependencies are all Python packages (yay!), though many of them
have non-Python dependencies. These are the direct dependencies. You will have
to find out and choose how to install them yourself. I don't know the minimum
version requirements, but I expect any Linux distro package manager to have
sufficiently up-to-date versions.

- [PyQt](http://www.riverbankcomputing.com/software/pyqt/intro) (4 only because
  of pyqtgraph)
- [scipy and numpy](http://www.scipy.org/)
- [scikit-learn](http://scikit-learn.sourceforge.net/stable/)
- [matplotlib](http://matplotlib.org/)
- [pyqtgraph](http://pyqtgraph.org/)
- [pydaqflex](https://github.com/torfbolt/PyDAQFlex)
