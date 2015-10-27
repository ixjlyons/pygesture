import time
import socket
import numpy as np

try:
    import daqflex
except ImportError:
    pass


class Daq(object):
    """
    A base class which fakes DAQ device functionality by generating random
    data.
    """

    def __init__(self, rate, input_range, channel_range, samples_per_read):
        self.rate = rate
        self.input_range = input_range
        self.samples_per_read = samples_per_read

        self.set_channel_range(channel_range)

    def start(self):
        pass

    def read(self):
        d = 0.2*self.input_range*(
            np.random.rand(self.num_channels, self.samples_per_read) - 0.5)
        time.sleep(float(self.samples_per_read/self.rate))
        return d

    def stop(self):
        pass

    def set_channel_range(self, channel_range):
        self.num_channels = channel_range[1] - channel_range[0] + 1


class MccDaq(Daq):
    """
    Access to data read by a Measurement Computing DAQ.

    Parameters
    ----------
    rate : int
        The sampling rate in Hz
    input_range : int
        Input range for the DAQ (+/-) in volts
    channel_range : tuple with 2 ints
        DAQ channels to use, e.g. (lowchan, highchan) obtains data from
        channels lowchan through highchan
    samples_per_read : int
        Number of samples per channel to read in each read operation

    Examples
    --------
    This is a basic example of how to set up the DAQ, read some data, and
    finish.

    >>> from pygesture import daq
    >>> dev = daq.MccDaq(2048, 1, (0, 1), 1024)
    >>> dev.initialize()
    >>> dev.start()
    >>> data = dev.read()
    >>> dev.close()
    """

    def __init__(self, rate, input_range, channel_range, samples_per_read):
        self.rate = rate
        self.input_range = input_range
        self.channel_range = channel_range
        self.samples_per_read = samples_per_read

        self.initialize()

    def initialize(self):
        self.device = daqflex.USB_1608G()

        self.device.send_message("AISCAN:XFRMODE=BLOCKIO")
        self.device.send_message("AISCAN:SAMPLES=0")
        self.device.send_message("AISCAN:BURSTMODE=ENABLE")
        self.device.send_message("AI:CHMODE=SE")

        self.device.send_message("AISCAN:RATE=%s" % self.rate)
        self.device.send_message("AISCAN:RANGE=BIP%sV" % self.input_range)

        self.set_channel_range(self.channel_range)

    def start(self):
        """
        Starts the DAQ so it begins reading data. read() should be called as
        soon as possible.
        """
        self.device.flush_input_data()
        self.device.send_message("AISCAN:START")

    def read(self):
        """
        Waits for samples_per_read samples to come in, then returns the data
        in a numpy array. The size of the array is (NUM_CHANNELS,
        SAMPLES_PER_READ).
        """
        data = self.device.read_scan_data(
            self.samples_per_read*self.num_channels, self.rate)

        data = np.array(data, dtype=np.float)
        data = np.reshape(data, (-1, self.num_channels)).T
        for i in range(self.num_channels):
            data[i, :] = self.device.scale_and_calibrate_data(
                data[i, :],
                -self.input_range,
                self.input_range,
                self.calibration_data[i])
        data = data / float(self.input_range)

        return data

    def stop(self):
        """
        Stops the DAQ. It needs to be started again before reading.
        """
        try:
            self.device.send_message("AISCAN:STOP")
        except:
            print('warning: DAQ could not be stopped')
            pass

    def set_channel_range(self, channel_range):
        self.channel_range = channel_range

        self.calibration_data = []
        for ch in range(channel_range[0], channel_range[1]+1):
            self.calibration_data.append(self.device.get_calib_data(ch))

        self.num_channels = len(self.calibration_data)

        self.device.send_message(
            "AISCAN:LOWCHAN={0}".format(channel_range[0]))
        self.device.send_message(
            "AISCAN:HIGHCHAN={0}".format(channel_range[1]))


class TrignoDaq(object):
    """
    Access to data served by Trigno Control Utility for the Delsys Trigno
    wireless EMG system. TCU is Windows-only, but this class can be used to
    stream data from it on another machine. TCU runs a TCP/IP server, with EMG
    data from the sensors on one port and accelerometer data on another. Only
    EMG data retrieval is currently implemented.

    Parameters
    ----------
    addr : str
        IP address the TCU server is running on
    channel_range : tuple with 2 ints
        Sensor channels to use, e.g. (lowchan, highchan) obtains data from
        channels lowchan through highchan
    samples_per_read : int
        Number of samples per channel to read in each read operation

    Examples
    --------
    This is a basic example of how to set up the DAQ, read some data, and
    finish.

    >>> from pygesture import daq
    >>> dev = daq.TrignoDaq('127.0.0.1', (0, 1), 1024)
    >>> dev.initialize()
    >>> dev.start()
    >>> data = dev.read()
    >>> dev.close()
    """

    """EMG data sample rate. Cannot be changed."""
    RATE = 2000
    """Port the EMG server runs on, specified by TCU."""
    PORT = 50041
    """Minimum recv size in bytes (16 sensors * 4 bytes/channel)."""
    MIN_RECV_SIZE = 64
    """Command string termination."""
    COMM_TERM = '\r\n\r\n'

    def __init__(self, addr, channel_range, samples_per_read):
        self.addr = addr
        self.channel_range = channel_range
        self.samples_per_read = samples_per_read

    def start(self):
        self.socket = socket.create_connection((self.addr, self.PORT))

        self.socket.send(TrignoDaq._cmd('START'))
        reply = self.socket.recv(128)

    @staticmethod
    def _cmd(command):
        return "{}{}".format(command, COMM_TERM)

