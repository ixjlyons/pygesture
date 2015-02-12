import numpy as np


def mav(x):
    """
    Calculates the mean absolute value of a signal.

    Parameters
    ----------
    x : ndarray
        The signal (can be multidimensional, in which case the MAV is
        calculated along columns)

    Returns
    -------
    y : ndarray
        The mean absolute value of each channel of the input.
    """
    y = np.mean(np.absolute(x), 0)
    return y


def wl(x):
    """
    Calculates the waveform length of a signal. Waveform length is just the
    sum of the absolute value of all deltas (between adjacent taps) of a
    signal.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate WL for. If multidimensional, WL is
        calculated along columns.

    Returns
    -------
    y : ndarray
        The waveform length of each channel of the input.
    """
    x2 = np.vstack((x[0, :], x[:-1, :]))
    y = np.sum(np.absolute(x - x2), 0)
    return y


def zc(x, thresh):
    """
    Calculates the number of zero crossings in a signal, subject to a threshold
    for discarding noisy fluctuations above and below zero.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate ZC for. If multidimensional, ZC is
        calculated along columns.
    thresh : float
        The threshold for discriminating true zero crossings from those caused
        by noise.

    Returns
    -------
    y : ndarray
        The number of zero crossings in each channel of the input.
    """
    xrows, xcols = x.shape
    y = np.zeros(xcols)
    for i in range(xcols):
        for j in range(1, xrows):
            if ((x[j, i] > 0 and x[j-1, i] < 0) or
                    (x[j, i] < 0 and x[j-1, i] > 0)):
                if np.absolute(x[j, i] - x[j-1, i]) > thresh:
                    y[i] += 1
    return y


def ssc(x, thresh):
    """
    Calculates the number of slope sign changes in a signal, subject to a
    threshold for discarding noisy fluctuations.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate SSC for. If multidimensional, SSC is
        calculated along columns.
    thresh : float
        The threshold for discriminating true slope sign changes from those
        caused by noise.

    Returns
    -------
    y : ndarray
        The number of slope sign changes in each channel of the input.
    """
    xrows, xcols = x.shape
    y = np.zeros(xcols)
    for i in range(xcols):
        for j in range(1, xrows-1):
            if ((x[j, i] > x[j-1, i] and x[j, i] > x[j+1, i]) or
                    (x[j, i] < x[j-1, i] and x[j, i] < x[j+1, i])):
                if (np.absolute(x[j, i] - x[j-1, i]) > thresh or
                        np.absolute(x[j, i] - x[j+1, i]) > thresh):
                    y[i] += 1
    return y


def spectral_moment(x, n):
    """
    Calculates the nth spectral moment of a signal.

    Parameters
    ----------
    x : ndarray
        The raw signal. If multidimensional, the moment is calculated for each
        column.
    n : int
        The order of the moment to take. Should be even and >= 0.
    """
    xrows, xcols = x.shape
    y = np.zeros(xcols)

    if n % 2 != 0:
        return y

    # special case, zeroth order moment is just the power
    if n == 0:
        y = np.sum(np.multiply(x, x), axis=0)

    else:
        y = spectral_moment(np.diff(x, int(n/2), axis=0), 0)

    return y


def khushaba_set(x, u=0):
    """
    Calcuates a set of 5 features introduced by Khushaba et al. at ISCIT 2012.
    They are:
        1. log of the 0th order spectral moment
        2. log of normalized 2nd order spectral moment (m2 / m0^u)
        3. log of normalized 4th order spectral moment (m4 / m0^(u+2))
        4. log of the sparseness (see paper)
        5. log of the irregularity factor / waveform length (see paper)

    Parameters
    ----------
    x : ndarray
        Raw signal. Each feature in the set is calculated for each column.
    u : int, optional (default = 0)
        Used in the exponent of m0 for normalizing higher-orer moments
    """
    m0 = spectral_moment(x, 0)
    m2 = spectral_moment(x, 2)
    m4 = spectral_moment(x, 4)
    S = m0 / np.sqrt((m0-m2)*(m0-m4))
    IF = np.sqrt(m2**2 / (m0*m4))
    WL = wl(x)

    return np.hstack((
        np.log(m0),
        np.log(m2 / m0**2),
        np.log(m4 / m0**4),
        np.log(S),
        np.log(IF / WL)))
