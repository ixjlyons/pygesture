"""

avg_group:
    name: name of the group (str)
    configs: list of train/test pairs
        sid_list_train: list of train SIDs for this config (list of str)
        sid_list_test: list of test SIDs for this config (list of str)

cv_group:
    name: name of the group (str)
    n_train: number of SIDs to use for training (int)
    sid_list: list of SIDs to use for cross validation (list of str)

clf_dict:
    name: name of the classifier (str)
    sid_list_train: list of SIDs to use for training (list of str)
    sid_list_test: list of SIDs to use for testing (list of str)

"""

import numpy as np

from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import LeavePOut

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from pygesture import processing


def run_single(rootdir, pids, clf_dict, clf=None, label_dict=None):
    """
    Runs a single batch classifier.

    Parameters
    ----------
    rootdir : str
        The root directory of the data
    pids : list of str
        The participant ID to run the test for
    clf_dict : dict
        A single_clf dictionary containing the following three keys: 'name',
        'sid_list_train' (list of session IDs for training the classifier), and
        'sid_list_test' (list of session IDs for testing the classifier).
    clf : sklearn classifier (default=None)
        An initialized (but not trained) classifier object, providing `fit()`
        and `predict()` methods. Default is `None`, which means
        `sklearn.lda.LDA` is used.
    label_dict: dict in the form 'int: (str, str)' (default=None)
        Mapping from class label (int) to a tuple including an abbreviation
        and a full name for each clss. Default is None, which means the
        integer labels contained in the data are given to the ConfusionMatrix
        returned.

    Returns
    -------
    cm : ConfusionMatrix
        The results of the classification test.

    Examples
    --------
    >>> from pygesture import classification
    >>> clf_dict = {
            'name': 'arm',
            'sid_list_train': ['arm1', 'arm2'],
            'sid_list_test': ['arm3', 'arm4']}
    >>> cm = classification.run_single('./data', ['p0'], clf_dict)
    >>> print(cm.get_avg_accuracy())
    0.9782919472
    """
    cm_list = []
    for pid in pids:
        data_train = processing.get_session_data(
            rootdir, pid, clf_dict['sid_list_train'])
        data_test = processing.get_session_data(
            rootdir, pid, clf_dict['sid_list_test'])

        if label_dict is not None:
            (X_train, y_train) = select_data(data_train, label_dict.keys())
            (X_test, y_test) = select_data(data_test, label_dict.keys())
        else:
            (X_train, y_train) = data_train
            (X_test, y_test) = data_test

        lid = np.unique(y_train.astype(int))
        if label_dict is None:
            labels = [str(l) for l in lid]
        else:
            labels = [label_dict[l][0] for l in lid]

        (X_train, X_test) = condition_data(X_train, X_test)

        if clf is None:
            clf = LDA()

        y_pred = clf.fit(X_train, y_train).predict(X_test)
        mat = confusion_matrix(y_test, y_pred)

        cm_list.append(ConfusionMatrix(mat, labels, name=clf_dict['name']))

    return average_confusion_matrix(cm_list)


def run_avg(rootdir, pids, avg_group, **kwargs):
    """Runs several train/test pairs and averages the results.

    The data is specified as a set of pairs of train/test data. Each pair is
    evaulated for classification accuracy, and the accuracy for each pair is
    then averaged for the result.

    Parameters
    ----------
    rootdir : str
        The root directory of the data
    pids : list of str
        The participant IDs to run the test for
    avg_group : dict
        The avg_group dict specifying the session IDs to test

    Returns
    -------
    cm : ConfusionMatrix
        The results of the classification test.

    Examples
    --------
    >>> from pygesture import classification
    >>> clf_dict = {
            'name': 'arm',
            'configs': [
                {
                    'sid_list_train': ['arm1', 'arm2'],
                    'sid_list_test': ['arm3', 'arm4']
                },
                {
                    'sid_list_train': ['arm1', 'arm3'],
                    'sid_list_test': ['arm2', 'arm4']
                }]}
    >>> cm = classification.run_avg('./data', ['p0'], clf_dict)
    >>> print(cm.get_avg_accuracy())
    0.872957201
    """
    cm_list = []
    for pid in pids:
        cm_sub = []
        for config in avg_group['configs']:
            config['name'] = avg_group['name']
            cm_sub.append(run_single(rootdir, [pid], config, **kwargs))

        cm_list.append(average_confusion_matrix(cm_sub))

    return average_confusion_matrix(cm_list)


def run_cv(rootdir, pids, cv_group, **kwargs):
    """Runs a group of sessions through leave-p-out cross validation.

    The data is specified as a list of session IDs which is split into groups
    training and testing data. A parameter (n_train) specifies how many of the
    SIDs to use for training in each group. The groups are formed by selecting
    n_train of the sessions for training and using the rest for testing. Each
    possible group is formed, a classifier is built and tested for each, and
    the average performance is given as the result.

    Parameters
    ----------
    rootdir : str
        The root directory of the data
    pids : list of str
        The participant IDs to run the test for
    cv_group : dict
        The cv_group dict specifying the session IDs and n_train

    Returns
    -------
    cm : ConfusionMatrix
        The results fo the classification test.

    Examples
    --------
    >>> from pygesture import classification
    >>> clf_dict = {
            'name': 'arm',
            'n_train': 2,
            'sid_list': ['arm1', 'arm2', 'arm3', 'arm4']}
    >>> cm = classification.run_cv('./data', ['p0'], clf_dict)
    >>> print(cm.get_avg_accuracy())
    0.92847295
    """
    cm_list = []
    for pid in pids:
        sid_list = cv_group['sid_list']
        n = len(sid_list)
        p = n - cv_group['n_train']
        lpo = LeavePOut(n, p=p)
        cm_sub = []
        for idx_train, idx_test in lpo:
            clf_dict = {
                'name': cv_group['name'],
                'sid_list_train': [sid_list[i] for i in idx_train],
                'sid_list_test': [sid_list[i] for i in idx_test]}
            cm_sub.append(run_single(rootdir, [pid], clf_dict, **kwargs))

        cm_list.append(average_confusion_matrix(cm_sub))

    return average_confusion_matrix(cm_list)


def select_data(data, labels):
    """Extracts only data with the given class labels.

    Parameters
    ----------
    data : 2-tuple
        Data in the form (X, y), where X holds the feature vectors and y holds
        the labels.
    labels : array
        Integer labels to select, matched to elements of y for masking.

    Returns
    -------
    data : 2-tuple
        Data in the same form as the input corresponding to the specified
        labels only.
    """
    X, y = data
    mask = np.zeros(y.shape, dtype=bool)
    for l in labels:
        mask |= (y == l)
    return (X[mask], y[mask])


def average_confusion_matrix(cm_list):
    mat = np.sum(cm.data for cm in cm_list)
    cm = ConfusionMatrix(mat, cm_list[0].labels, cm_list[0].name)
    return cm


def accuracy_std(cm_list):
    diags = np.array([cm.data_norm.diagonal(0) for cm in cm_list])
    std = np.std(diags, axis=0)
    return std


def condition_data(X_train, X_test):
    means = np.mean(X_train, 0)
    stds = np.std(X_train, 0)

    X_train = X_train - means
    X_train = X_train / stds.T

    X_test = X_test - means
    X_test = X_test / stds.T

    return (X_train, X_test)


def generate_plot(cm, acc, labels, title, fig=None, savepath=None):
    if fig is None:
        fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(cm, cmap='hot_r')

    lbls = []
    for idx, label in enumerate(labels):
        num = round(cm[idx, idx], 2)
        if num > 0.5:
            color = 'w'
        else:
            color = 'k'
        ax.text(idx, idx, str(num), color=color, va='center', ha='center')
        lbls.append(label)

    notes = np.where(cm > 0.01)
    for i in range(np.size(notes[0])):
        x, y = notes[0][i], notes[1][i]
        if x != y:
            num = round(cm[x, y], 2)
            if num > 0.5:
                color = 'w'
            else:
                color = 'k'
            ax.text(y, x, str(num), color=color, va='center', ha='center')

    ax.set_title(title + (': %.2f' % (acc*100)) + '% accuracy')
    ml = MultipleLocator(1)
    ax.xaxis.set_major_locator(ml)
    ax.yaxis.set_major_locator(ml)
    ax.set_xticklabels(['']+lbls)
    ax.set_yticklabels(['']+lbls)
    if savepath:
        plt.savefig(savepath + '/' + title + '.pdf', bbox_inches='tight')
    else:
        plt.show()


class ConfusionMatrix():

    def __init__(self, mat, labels, name="confusion matrix"):
        self.labels = labels
        self.name = name
        self.data = mat
        self.data_norm = self.get_normalized()
        self.accuracy = self.get_avg_accuracy()

    def get_normalized(self):
        row_sums = np.sum(self.data, 1)
        return self.data / row_sums[:, None]

    def get_avg_accuracy(self):
        num_instances = np.sum(self.data, (0, 1))
        num_correct = np.sum(self.data.diagonal(0))
        return num_correct / float(num_instances)

    def show(self, fig=None):
        generate_plot(self.data_norm, self.accuracy, self.labels, self.name,
                      fig=fig)

    def print_avg(self, normalized=True):
        print("--")
        print("Classifer: " + self.name)
        print("--")
        if normalized:
            np.set_printoptions(precision=2)
            print(self.data_norm)
        else:
            print(self.data)
