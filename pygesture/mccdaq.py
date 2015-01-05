import numpy as np
import daqflex


class MccDaq:
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

    >>> import mccdaq
    >>> daq = mccdaq.MccDaq(2048, 1, (0, 1), 1024)
    >>> daq.start()
    >>> data = daq.read()
    >>> daq.close()
    """

    def __init__(self, rate, input_range, channel_range, samples_per_read):
        self.device = daqflex.USB_1608G()

        self.rate = rate
        self.input_range = input_range
        self.samples_per_read = samples_per_read

            
        self.device.send_message("AISCAN:XFRMODE=BLOCKIO")
        self.device.send_message("AISCAN:SAMPLES=0")
        self.device.send_message("AISCAN:BURSTMODE=ENABLE")
        self.device.send_message("AI:CHMODE=SE")

        self.device.send_message("AISCAN:RATE={0}".format(rate))
        self.device.send_message("AISCAN:RANGE=BIP{0}V".format(input_range))

        self.set_channel_range(channel_range)

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
            data[i, :] = self.device.scale_and_calibrate_data(data[i, :],
                -self.input_range, self.input_range,
                self.calibration_data[i])
        data = data / float(self.input_range)

        return data

    def stop(self):
        """
        Stops the DAQ. It needs to be started again before reading.
        """
        self.device.send_message("AISCAN:STOP")

    def set_channel_range(self, channel_range):
        self.channel_range = channel_range

        self.calibration_data = []
        for ch in range(channel_range[0], channel_range[1]+1):
            self.calibration_data.append(self.device.get_calib_data(ch))

        self.num_channels = len(self.calibration_data)

        self.device.send_message("AISCAN:LOWCHAN={0}".format(channel_range[0]))
        self.device.send_message("AISCAN:HIGHCHAN={0}".format(channel_range[1]))
