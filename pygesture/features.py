import numpy as np

from pygesture.pipeline import PipelineBlock


class FeatureExtractor(PipelineBlock):

    def __init__(self, features, n_channels):
        super(FeatureExtractor, self).__init__()
        self.features = features
        self.n_channels = n_channels
        self.n_features = n_channels*sum(
            [f.dim_per_channel for f in self.features])

        self.output = np.zeros(self.n_channels*self.n_features)

    def process(self, data):
        # TODO use pre-allocated output array instead of hstack
        return np.hstack([f.compute(data) for f in self.features])

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.features
        )


class MAV(object):
    """
    Calculates the mean absolute value of a signal.
    """

    def __init__(self):
        self.dim_per_channel = 1

    def compute(self, x):
        y = np.mean(np.absolute(x), axis=0)
        return y


class WL(object):
    """
    Calculates the waveform length of a signal. Waveform length is just the
    sum of the absolute value of all deltas (between adjacent taps) of a
    signal.
    """

    def __init__(self):
        self.dim_per_channel = 1

    def compute(self, x):
        y = np.sum(np.diff(x, axis=0), axis=0)
        return y


class ZC(object):
    """
    Calculates the number of zero crossings in a signal, subject to a threshold
    for discarding noisy fluctuations above and below zero.

    Parameters
    ----------
    thresh : float (default=0.0)
        The threshold for discriminating true zero crossings from those caused
        by noise.
    use_sm : bool (default=False)
        Specifies if spectral moments should be used for the computation. This
        is much faster, but the threshold is not taken into account, making it
        potentially affected by noise.
    """

    def __init__(self, thresh=0.0, use_sm=False):
        self.dim_per_channel = 1
        self.thresh = thresh
        self.use_sm = use_sm

    def compute(self, x):
        if self.use_sm:
            y = np.sqrt(
                SpectralMoment(2).compute(x) / SpectralMoment(0).compute(x))

        else:
            xrows, xcols = x.shape
            y = np.zeros(xcols)
            for i in range(xcols):
                for j in range(1, xrows):
                    if ((x[j, i] > 0 and x[j-1, i] < 0) or
                            (x[j, i] < 0 and x[j-1, i] > 0)):
                        if np.absolute(x[j, i] - x[j-1, i]) > self.thresh:
                            y[i] += 1

        return y


class SSC(object):
    """
    Calculates the number of slope sign changes in a signal, subject to a
    threshold for discarding noisy fluctuations.

    Parameters
    ----------
    thresh : float (default=0.0)
        The threshold for discriminating true slope sign changes from those
        caused by noise.
    use_sm : bool (deafult=False)
        Specifies if spectral moments should be used for the computation. This
        is much faster, but the threshold is not taken into account, making it
        potentially affected by noise.
    """

    def __init__(self, thresh=0.0, use_sm=False):
        self.dim_per_channel = 1
        self.thresh = thresh
        self.use_sm = use_sm

    def compute(self, x):
        if self.use_sm:
            y = np.sqrt(
                SpectralMoment(4).compute(x) / SpectralMoment(2).compute(x))

        else:
            xrows, xcols = x.shape
            y = np.zeros(xcols)
            for i in range(xcols):
                for j in range(1, xrows-1):
                    if ((x[j, i] > x[j-1, i] and x[j, i] > x[j+1, i]) or
                            (x[j, i] < x[j-1, i] and x[j, i] < x[j+1, i])):
                        if (np.absolute(x[j, i]-x[j-1, i]) > self.thresh or
                                np.absolute(x[j, i]-x[j+1, i]) > self.thresh):
                            y[i] += 1
        return y


class SpectralMoment(object):
    """
    Calculates the nth-order spectral moment.

    Parameters
    ----------
    n : int
        The spectral moment order. Should be even and greater than or equal to
        zero.
    """

    def __init__(self, n):
        self.dim_per_channel = 1
        self.n = n

    def compute(self, x):
        xrows, xcols = x.shape
        y = np.zeros(xcols)

        if self.n % 2 != 0:
            return y

        # special case, zeroth order moment is just the power
        if self.n == 0:
            y = np.sum(np.multiply(x, x), axis=0)

        else:
            y = SpectralMoment(0).compute(np.diff(x, int(self.n/2), axis=0))

        return y


class KhushabaSet(object):
    """
    Calcuates a set of 5 features introduced by Khushaba et al. at ISCIT 2012.
    (see reference [1]). They are:
        1. log of the 0th order spectral moment
        2. log of normalized 2nd order spectral moment (m2 / m0^u)
        3. log of normalized 4th order spectral moment (m4 / m0^(u+2))
        4. log of the sparseness (see paper)
        5. log of the irregularity factor / waveform length (see paper)

    Parameters
    ----------
    u : int (default=0)
        Used in the exponent of m0 for normalizing higher-orer moments

    References
    ----------
    .. [1] `R. N. Khushaba, L. Shi, and S. Kodagoda, "Time-dependent spectral
        features for limb position invariant myoelectric pattern recognition,"
        Communications and Information Technologies (ISCIT), 2012 International
        Symposium on, 2012.`
    """

    def __init__(self, u=0):
        self.dim_per_channel = 5
        self.u = u

    def compute(self, x):
        xrows, xcols = x.shape
        y = np.zeros(self.dim_per_channel*xcols)
        # TODO fill this instead of using hstack

        m0 = SpectralMoment(0).compute(x)
        m2 = SpectralMoment(2).compute(x)
        m4 = SpectralMoment(4).compute(x)
        S = m0 / np.sqrt(np.abs((m0-m2)*(m0-m4)))
        IF = np.sqrt(m2**2 / (m0*m4))

        return np.hstack((
            np.log(m0),
            np.log(m2 / m0**2),
            np.log(m4 / m0**4),
            np.log(S),
            np.log(IF / WL().compute(x))))


class SampEn(object):
    """
    Calculates the sample entropy of time series data. See reference [1].

    The basic idea is to take all possible m-length subsequences of the
    time series and count the number of these subsequences whose Chebyshev
    distance from all other subsequences is less than the tolerance parameter,
    r (self-matches excluded). This is repeated for (m+1)-length subsequences,
    and SampEn is given by the log of the number of m-length matches divided
    by the number of (m+1)-length matches.

    This feature can have some issues if the tolerance r is too low and/or the
    subsequence length m is too high. A typical value for r is apparently
    0.2*std(x).

    Parameters
    ----------
    m : int
        Length of sequences to compare (>1)
    r : float
        Tolerance for counting matches.

    References
    ----------
    .. [1] `J. S. Richman and J. R. Moorman, "Physiological time series
        analysis using approximate entropy and sample entropy," American
        Journal of Physiology -- Heart and Circulatory Physiology, vol. 278
        no. 6, 2000.`
    """

    def __init__(self, m, r):
        self.dim_per_channel = 1
        self.m = m
        self.r = r

    def compute(self, x):
        xrows, xcols = x.shape
        y = np.zeros(xcols)
        m = self.m
        N = xrows

        for c in range(xcols):
            correl = np.zeros(2) + np.finfo(np.float).eps

            xmat = np.zeros((m+1, N-m+1))
            for i in range(m):
                xmat[i, :] = x[i:N-m+i+1, c]
            # handle last row separately
            xmat[m, :-1] = x[m:N, c]
            xmat[-1, -1] = 10*np.max(xmat)  # something that won't get matched

            for mc in [m, m+1]:
                count = 0
                for i in range(N-mc-1):
                    dist = np.max(
                        np.abs(xmat[:mc, i+1:] - xmat[:mc, i][:, np.newaxis]),
                        axis=0)

                    count += np.sum(dist <= self.r)

                correl[mc-m] = count

            y[c] = np.log(correl[0] / correl[1])

        return y
