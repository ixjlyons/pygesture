import random
import itertools


class TACSession(object):

    def __init__(self, gestures, simultaneous=1, n_repeat=1):
        self.gestures = gestures
        self.simultaneous = simultaneous
        self.n_repeat = n_repeat

        if simultaneous == 1:
            # _gesture_combinations() can handle this case, but it returns a
            # list of 1-tuples
            t = list(gestures)
        else:
            t = list(_gesture_combinations(gestures, k=simultaneous))
        self.targets = t

        self.trials = _generate_trials(self.targets, n_repeat=n_repeat)


def _gesture_combinations(gestures, k=1):
    """
    Generate all combinations of k simultaneous gestures, but filter out those
    containing gestures of the same DOF (e.g. no simultaneous elbow flexion and
    extension). If there are n gestures and k are chosen simultaneously, there
    are 2*(nCk) combinations (2 gestures per DOF).

    Parameters
    ----------
    dofs : dict {gesture: dof}
        Dictionary mapping each gesture to a degree of freedom. Pairs of
        of gestures (e.g. elbow flexion/extension) should have the same dof.
    k : int, default 1
        Number of gestures to include in each combination.
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
