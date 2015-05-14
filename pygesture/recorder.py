import os
import random
import shutil

import numpy as np

from pygesture import filestruct

from PyQt4 import QtCore


class RecordThread(QtCore.QThread):

    update_sig = QtCore.pyqtSignal(np.ndarray)
    finished_sig = QtCore.pyqtSignal(np.ndarray)
    prediction_sig = QtCore.pyqtSignal(object)

    def __init__(self, daq):
        QtCore.QThread.__init__(self, parent=None)
        self.daq = daq

        self.continuous = True
        self.triggers_per_record = 0
        self.running = False
        self.pipeline = None

    def run(self):
        self.running = True

        if self.continuous:
            self.run_continuous()
        else:
            self.run_fixed()

    def run_continuous(self):
        self.daq.start()

        while self.running:
            d = self.daq.read()
            if self.pipeline is not None:
                y = self.pipeline.process(d.T)
                self.prediction_sig.emit(y)

            self.update_sig.emit(d)

        self.daq.stop()

    def run_fixed(self):
        spr = self.daq.samples_per_read
        data = np.zeros((self.daq.num_channels, spr*self.triggers_per_record))
        self.daq.start()
        for i in range(self.triggers_per_record):
            d = self.daq.read()

            data[:, i*spr:(i+1)*spr] = d
            self.update_sig.emit(d)

        self.daq.stop()
        self.finished_sig.emit(data)

    def set_continuous(self):
        self.continuous = True

    def set_fixed(self, triggers_per_record=None):
        if triggers_per_record is not None:
            self.triggers_per_record = triggers_per_record
        self.continuous = False

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def kill(self):
        self.running = False
        self.wait()
