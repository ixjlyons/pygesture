import random
import itertools


class TACSession(object):
    """
    Target Achievement Control test session.

    Parameters
    ----------
    gestures : dict {gesture: dof}
        Dictionary mapping each gesture to a degree of freedom. Pairs of
        of gestures (e.g. elbow flexion/extension) should have the same dof.
    simul : int, default=1
        Number of DOFs for each target.
    rep : int, default=1
        Number of repetitions of each possible target.
    timeout : number, default=0
        Maximum trial duration, in seconds. Zero means no timeout.
    tol : number, default=10
        Error tolerance for each joint (DOF), in degrees.
    dwell : number, default=0
        Amount of time the joints must be within `tol` to complete a trial, in
        seconds.

    Attributes
    ----------
    targets : list
        A list of tuples, where each tuple specifies a set of gestures for the
        given trial (each tuple has `simul` elements).
    trials : list
        A list of the same tuples as in `targets`, but repeated (specified by
        `rep`) and in randomized order.
    """

    def __init__(self, gestures, simul=1, rep=1, timeout=0, tol=10, dwell=0):
        self.gestures = gestures
        self.simul = simul
        self.rep = rep
        self.timeout = timeout
        self.tol = tol
        self.dwell = dwell

        t = list(_gesture_combinations(gestures, k=simul))

        self.targets = t
        self.trials = _generate_trials(self.targets, n_repeat=rep)


def _gesture_combinations(gestures, k=1):
    """
    Generate all combinations of k simultaneous gestures, but filter out those
    containing gestures of the same DOF (e.g. no simultaneous elbow flexion and
    extension). If there are n gestures and k are chosen simultaneously, there
    are 2*(nCk) combinations (2 gestures per DOF).

    Parameters
    ----------
    gestures : dict {gesture: dof}
        Dictionary mapping each gesture to a degree of freedom. Pairs of
        of gestures (e.g. elbow flexion/extension) should have the same dof.
    k : int, default 1
        Number of gestures to include in each combination.

    Returns
    -------
    comb : generator of tuples
        The combinations of `k` elements from exclusive DOFs in `gestures`.
    """
    for comb in itertools.combinations(gestures, r=k):
        # only yield combination if k DOFs are represented
        if len(set(gestures[gest] for gest in comb)) == k:
            yield comb


def _shuffle(x):
    """
    Shuffles an iterable, returning a copy (random.shuffle shuffles in place).
    """
    x = list(x)
    random.shuffle(x)
    return x


def _generate_trials(trial_set, n_repeat=1):
    """
    Generates a trial sequence where trial_set is shuffled and repeated
    n_repeat times.
    """
    return list(itertools.chain.from_iterable(
        _shuffle(trial_set) for i in range(n_repeat)))
