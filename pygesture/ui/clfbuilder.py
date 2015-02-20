#from PySide import QtGui, QtCore
from PyQt4 import QtGui, QtCore

from sklearn.lda import LDA

from pygesture import filestruct
from pygesture import settings as st


class ClassifierBuilderDialog(QtGui.QDialog):
    """
    QDialog for choosing training data sessions for a classifier.
    """

    def __init__(self):
        super(ClassifierBuilderDialog, self).__init__()

        # build ui elements
        self.create_participant_selector()
        self.create_session_selector()
        self.create_button_box()

        # build layout
        self.layout = QtGui.QVBoxLayout()

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.participant_label, 1, 0)
        self.grid.addWidget(self.participant_selector, 1, 1)
        self.grid.addWidget(self.session_label, 2, 0)
        self.grid.addWidget(self.session_selector, 2, 1, 4, 1)

        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.button_box)

        # signals
        self.participant_selector.currentIndexChanged.connect(self.update_pid)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # final setup
        self.update_pid(0)
        self.setLayout(self.layout)
        self.setWindowTitle("build classifier")

    def create_participant_selector(self):
        self.participant_label = QtGui.QLabel('Participant:')
        self.participant_selector = QtGui.QComboBox()
        self.pid_list = filestruct.get_participant_list(st.DATA_ROOT)
        self.participant_selector.addItems(self.pid_list)

    def create_session_selector(self):
        self.session_label = QtGui.QLabel('Sessions:')
        self.session_selector = QtGui.QListWidget()

    def create_button_box(self):
        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

    def update_pid(self, index):
        self.pid = self.pid_list[index]
        self.session_selector.clear()
        self.sids = filestruct.get_session_list(st.DATA_ROOT, self.pid)
        for sid in self.sids:
            item = QtGui.QListWidgetItem(sid, self.session_selector)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

    def get_training_ids(self):
        sid_list = self.get_session_selections()
        return (self.pid, sid_list)

    def get_session_selections(self):
        l = []
        for i in xrange(self.session_selector.count()):
            item = self.session_selector.item(i)
            if item.checkState():
                l.append(item.text().encode('ascii', 'ignore'))
        return l


def train_classifier(pid, sid_list, clf=None):
    """
    Trains a classifier with data from the given participant and sessions. A
    classifier can be specified. If none is given, the default is LDA.

    Parameters
    ----------
    pid : string
        Participant ID
    sid_list : list of strings
        List of session IDs to train on
    clf : sklearn estimator object (default=sklearn.lda.LDA())

    Returns
    -------
    clf : estimator
        The classifier after being fit to the data. Now you can use
        clf.predict(input) to use the classifier for predictions.
    """
    (X, y) = filestruct.get_session_data(pid, sid_list)
    if clf is None:
        clf = LDA()
    clf.fit(X, y)
    return clf


def get_training_data():
    """
    Convenience method to open the ClassifierBuilderDialog in isolation,
    returning the participant and session IDs that are selected.

    Returns
    -------
    data : tuple (str, list)
        The participant ID and list of session IDs selected in the dialog.
    """
    qapp = QtCore.QCoreApplication.instance()
    if qapp is None:
        qapp = QtGui.QApplication([])
    dialog = ClassifierBuilderDialog()
    if dialog.exec_():
        return dialog.get_training_ids()
    else:
        return ('', [])


import sys
def main():
    app = QtGui.QApplication([])
    dialog = ClassifierBuilderDialog()
    dialog.show()
    sys.exit(app.exec_())
