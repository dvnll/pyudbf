import numpy as np
import math
import logging
import pprint


__all__ = ["UDBFHeader", "UDBFData"]


class UDBFHeader(object):

    """
    Data-class for meta-data of UDBFData.
    """

    def __init__(self, *,
                 udbf_version,
                 vendor,
                 sampling_rate,
                 number_of_channels,
                 variable_names,
                 variable_directions,
                 variable_types,
                 variable_units,
                 variable_precision,
                 channel_additional_data):

        self.udbf_version = udbf_version
        self.vendor = vendor
        self.sampling_rate = sampling_rate
        self.number_of_channels = number_of_channels
        self.variable_names = variable_names
        self.variable_directions = variable_directions
        self.variable_types = variable_types
        self.variable_units = variable_units
        self.variable_precision = variable_precision
        self.channel_additional_data = channel_additional_data

    def channel_variable(self, channel):
        return self.variable_names[channel]

    def channel_unit(self, channel):
        return self.variable_units[channel]

    @property
    def to_dictionary(self):
        """
        Adds all class variables whose name doesn't start with an underscore ("_") 
        to a dictionary.
        """
        temp_dict = {}
        for key in self.__dict__:
            if key[0] == "_":
                continue

            if isinstance(self.__dict__[key], dict):
                sdict = {}
                odict = self.__dict__[key]
                for kkey in odict:
                    sdict[str(kkey)] = odict[kkey]
                    temp_dict[str(key)] = sdict
                continue

            temp_dict[str(key)] = self.__dict__[key]

        return {self.name: temp_dict}

    def print(self):
        print("\nData header:\n")
        pprint.pprint(self.to_dictionary)


class UDBFData(object):
    """
    Data-class for data read as UDBF.
    """
    def __init__(self):

        pass
        #self.infile_id = "_infile"

    @property
    def n_points(self):
        return self._n_points

    @property
    def n_channels(self):
        return self._n_channels

    @property
    def channel_signals(self):
        channel_signals_id = "_channel_signals"
        if channel_signals_id not in self.__dict__:
            self._check_channel_signals()

        return self._channel_signals

    @property
    def runlength(self):
        return self._runlength
    
    @property
    def good_channels(self):
        good_channels_id = "_good_channels"
        if good_channels_id not in self.__dict__:
            self._check_channel_signals()

        return getattr(self, good_channels_id)

    @property
    def channel_states(self):
        channel_states_id = "_channel_states"
        if channel_states_id not in self.__dict__:
            self._check_channel_signals()

        translated = {}
        channel_states = getattr(self, channel_states_id)
        channel_names = self.header.variable_names

        for key in channel_states:
            channel_info = [channel_names[key], channel_states[key]]
            translated["channel_" + str(key)] = channel_info

        return translated

    @property
    def timestamps(self):
        return self._timestamps

    def _check_channel_signals(self):

        channel_status_message = "UDBFReader raw data check: "

        self._good_channels = []

        channel_signals = self.channel_signals
        self._channel_states = {i: [] for i in range(len(channel_signals))}

        zero_timestamps = {}

        for i, signal in enumerate(channel_signals):
            entries = len(signal)
            if entries == 0:
                status = channel_status_message + "No event in channel"
                self._channel_states[i].append(status)
                continue

            if self.header.variable_types[i] not in (1, 8):
                status = channel_status_message
                status += "Variable type "
                status += str(self.header.variable_types[i])
                status += " not known"
                self._channel_states[i].append(status)
                continue

            if self.header.variable_types[i] == 1:
                status = channel_status_message
                status += "State channel"
                if bool(signal[0]) is False:
                    status += " (LOW start)"
                else:
                    status += " (HIGH start)"
                self._channel_states[i].append(status)
                continue

            zero_timestamps[i] = np.where(signal == 0.0)

        self._zero_fraction_check(zero_timestamps, channel_status_message)

    def _zero_fraction_check(self, zero_timestamps, channel_status_message):

        zero_fraction_error = False
        for channel in zero_timestamps:
            if len(zero_timestamps[channel]) == 0:
                self._good_channels.append(channel)
                status = channel_status_message + "Data channel"
                self._channel_states[channel].append(status)
                continue

            if zero_fraction_error:
                break

            for time in zero_timestamps[channel]:
                if zero_fraction_error:
                    break

                for other_channel in zero_timestamps:
                    if zero_fraction_error:
                        break

                    if channel == other_channel:
                        continue

                    # Check whether same timestamp occurs
                    # in other channels

                    for other_time in zero_timestamps[other_channel]:
                        for index in time:
                            if index in other_time:
                                zero_fraction_error = True
                                break

        if zero_fraction_error is False:
            for channel in zero_timestamps:
                self._good_channels.append(channel)
                status = channel_status_message
                status += "Data channel"
                self._channel_states[channel].append(status)

        else:
            for channel in zero_timestamps:
                signal = self.channel_signals[channel]
                entries = len(signal)

                n_nonzero = np.count_nonzero(signal)

                zero_fraction = float(entries - n_nonzero) / float(entries)

                status = channel_status_message + "Zero fraction error"
                self._channel_states[channel].append(status)

                status = "Zero fraction: "
                status += "%.1E" % (zero_fraction * 100.) + " %"
                self._channel_states[channel].append(status)
                indices = np.where(signal == 0.0)
                timestamps = np.array(self.timestamps)
                times = timestamps[indices]
                if len(times) > 10:
                    delta = times[1:] - times[:-1]
                    delta = [d.total_seconds() for d in delta]
                    delta_mean = np.mean(delta)
                    delta_var = math.sqrt(np.var(delta, ddof=1))
                    status = "Time between zeros: ("
                    status += str(delta_mean) + " +- "
                    status += str(delta_var) + ") s"
                    self._channel_states[channel].append(status)
                else:
                    seconds_after_start = []
                    for time in times:
                        seconds = time - self.timestamps[0]
                        seconds_after_start.append(seconds.total_seconds())

                    text = "Zero signal events at "
                    text += str(seconds_after_start) + "s after runstart"
                    self._channel_states[channel].append(text)

    def to_ascii(self, outfile):

        amplitude_array = []

        channels = [c for c in range(self.n_channels)]

        for channel in channels:
            signal = self.channel_signal(channel)
            amplitude_array.append(signal)

        with open(outfile, "a+") as fout:
            first_line = "Sampling frequency: "
            first_line += str(self.header.sampling_rate) + "\n"
            
            fout.write(first_line)
            line = ""
            for i in channels:
                line += str(self.header.channel_variable(i).replace(" ", "_"))
                line += " "
            line += "\n"
            fout.write(line)

            n_events = len(amplitude_array[0])

            for i in range(n_events):
                line = ""
                for k in range(len(amplitude_array)):
                    line += str(amplitude_array[k][i])
                    line += " "
                line += "\n"
                fout.write(line)

    def channel_signal(self, channel):

        if "_channel_signals" not in self.__dict__:
            raise RuntimeError("Channel signals not set")
        if channel not in range(len(self.channel_signals)):
            raise RuntimeError("Requested channel doesn't exist")

        return self.channel_signals[channel]

    def _set_udbf_data(self, timestamps, signals, header):

        if len(timestamps) != len(signals):
            exit_state = "Signal lengths doesn't match timestamp length"
            raise RuntimeError(exit_state)

        if len(timestamps) == 0:
            exit_state = "Data contains no events"
            raise RuntimeError(exit_state)

        self._n_points = len(timestamps)
        self._channel_signals = np.transpose(signals)

        if len(self._channel_signals) > header.number_of_channels:
            exit_state = "Have more read-out channels"
            exit_state += " than expected from header"
            raise RuntimeError(exit_state)

        if len(self._channel_signals) < header.number_of_channels:
            exit_state = "Have less read-out channels than"
            exit_state += " expected from header"
            raise RuntimeError(exit_state)

        self._n_channels = header.number_of_channels

        self._timestamps = timestamps
        delta = self.timestamps[-1] - self.timestamps[0]
        self._runlength = delta.total_seconds()

        self.header = header
        self._check_channel_signals()


