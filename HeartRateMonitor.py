import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from detect_peaks import detect_peaks
import json

# Read the data ***********************************************


def is_csv(file_name):
    """Tests if the input file is a CSV

    Args:
        file_name: (string) name of the file

    Returns:
        Returns True if file is CSV, otherwise False

    Raises:
        TypeError: If file_name is not a CSV

    """
    if file_name.endswith(".csv"):
        return True
    elif not file_name.endswith(".csv"):
        raise TypeError("File is not a CSV file")
    return False


def read_ecg(file_name):
    """Reads the CSV file into numpy array

    Args:
        file_name: (string) name of the CSV file

    Returns:
        Returns numpy.array of the ECG data in the file

    Raises:
        TypeError: If file_name is not a CSV

    """
    if is_csv(file_name):
        ecg_data = np.genfromtxt(file_name, delimiter=",")
        return ecg_data


def is_data_not_float(data):
    """Tests if the input data is all floats or not

    Also used to tests if the x and y columns
    of the CSV data are of the same length

    Args:
        data: array of data to parse through

    Returns:
        Returns True if a NaN exists in the array.

    """
    data_good = any(np.isnan(t) for t in data)
    return data_good


def is_enough_data(data):
    """Tests if there is sufficient ECG data

    Args:
        data: 1D array of data to parse through

    Returns:
        Nothing is returned

    Raises:
        ValueError: If there are less than 25 data points

    """
    if len(data) < 25:
        raise ValueError("You need more than 25 data points")


def split_time_data(ecg_data):
    """Splits the time data from the ECG data

    Args:
        ecg_data: array of ECG datapoints

    Returns:
        Array of time data points

    Raises:
        TypeError: If there any data is non-numeric

    """
    time_data = ecg_data[:, 0]
    if is_data_not_float(time_data):
        raise TypeError('Time data is not all numeric')
    else:
        return time_data


def split_volt_data(ecg_data):
    """Splits the voltage data from the ECG data

    Args:
        ecg_data: array of ECG datapoints

    Returns:
        Array of voltage data points

    Raises:
        TypeError: If there any data is non-numeric

    """
    volt_data = ecg_data[:, 1]
    if is_data_not_float(volt_data):
        raise TypeError('Voltage data is not all numeric')
    else:
        return volt_data

# Process the data *******************************************


def yes_no(from_input):
    """Used to get user input as yes/no only

    Args:
        from_input: user's previous input

    Returns:
        None

    Raises:
        SystemExit: If user does not want to continue

    """
    answer = from_input
    if answer == "yes":
        return 'Continue!'
    elif answer == "no":
        raise SystemExit(0)
    while answer not in ("yes", "no"):
        answer = input("Enter yes or no: ")
        if answer == "yes":
            return 'Continue!'
        elif answer == "no":
            raise SystemExit(0)
        else:
            print("Please enter yes or no.")


def is_volt_data_in_range(voltage_extremes, stop_prompt = None):
    """Tests if the voltage data is reasonable

        Prompts user that data may not be trustworthy if any data
        is more than 5V or less than -5V. User decides to continue
        or not

    Args:
        voltage_extremes: The highest and lowest
        detected voltage data from the ECG data
        stop_prompt: Default is none, mostly used for unit testing

    Returns:
        None

    """
    if voltage_extremes[0] < -5:
        if stop_prompt is None:
            stop_prompt = input('Voltage below -5V detected. '
                                'This probably is not good data.'
                                ' Continue? yes/no')
        return yes_no(stop_prompt)
    elif voltage_extremes[1] > 5:
        if stop_prompt is None:
            stop_prompt = input('Voltage above 5V detected. '
                                'This probably is not good data.'
                                ' Continue? yes/no')
        return yes_no(stop_prompt)


def is_time_too_short(duration):
    """Tests if the ECG strip has sufficient time data

    Args:
        duration: the time of the last measured ECG data point

    Returns:
        None

    Raises:
        ValueError: At least 5 seconds of ECG data is needed

    """
    if duration < 5:
        raise ValueError("You need more than 5 seconds of ECG data")


def is_peaks_detected(num_beats):
    """Tests if any heartbeats are detected at all

    Args:
        num_beats: the number of heartbeats detected

    Returns:
        None

    Raises:
        ValueError: If there are no heartbeats detected

    """
    if num_beats == 0:
        raise ValueError("No heart beats detected in dataset")


def find_volt_extreme(volt_data):
    """Determines the highest and lowest voltages

    Args:
        volt_data: (array) the voltage part of the ECG data

    Returns:
        voltage_extremes: a tuple of the (minimum, maxiumum) voltage

    """
    max_volt = max(volt_data)
    min_volt = min(volt_data)
    voltage_extremes = (min_volt, max_volt)
    return voltage_extremes


def find_time_duration(time_data):
    """Determines the duration of the ECG strip

    Args:
        time_data: (array) the time part of the ECG data

    Returns:
        duration: (float) value of the last time point in ms

    """
    duration = time_data[-1]
    return duration


def find_number_beats(detected_peaks):
    """Determines the number of heartbeats in the ECG strip

    Args:
        detected_peaks: array of the indexes where a heartbeat
        was detected

    Returns:
        num_beats: (int) the number of heartbeats detected

    """
    num_beats = len(detected_peaks)
    return num_beats


# returns the time in ms of when the peaks occurred
def find_beat_times(time_data, detected_peaks):
    """Determines the time value when heartbeats occurred

    Args:
        time_data: (array) the time part of the ECG data
        detected_peaks: array of the indexes where a heartbeat
        was detected

    Returns:
        beats: (array) of time values where heartbeat detected

    """
    beats = time_data[detected_peaks]
    return beats


def specify_time(user_specified_time = None):
    """User specified time over which to measure the
    mean heart rate. Measured from the beginning of
    the time strip

    Asks the user to input a time interval. Raises
    a ValueError if the user gives anything but an integer
    Then defaults input to 60 seconds.

    Args:
        user_specified_time: This is just for unit testing. Do not change this

    Returns:
        user_specified_time: (int) integer value in seconds

    """
    if user_specified_time is None:
        user_specified_time = input('What time interval '
                                    'should I calculate the mean '
                                    'heart rate?\n'
                                    'Please enter a time in seconds:')
    try:
        user_specified_time = int(user_specified_time)
    except ValueError:
        print('I can only take integers. You had one job, '
              'and you messed it up. Going to default setting '
              'of 60 seconds')
        user_specified_time = 60
    return user_specified_time


# Input is the beats from find_beat_times
def find_avg_hr(time_of_beats, user_specified_time):
    """Determines the average heart rate over user
    specified amount of time.

    Args:
        time_of_beats: (array) of times when a heartbeat detected
        user_specified_time: (int) time interval to calculate
        average heart rate, user specified

    Returns:
        mean_hr_beat: (int) average heart rate, rounded to the
        nearest integer

    """
    num_beats = sum(i < user_specified_time for i in time_of_beats)
    if user_specified_time > time_of_beats[-1]:
        divisor_time = time_of_beats[-1]
    else:
        divisor_time = user_specified_time
    mean_hr_bpm = int(round(60/divisor_time*num_beats))
    return mean_hr_bpm


# Output to JSON****************************************
def create_metrics_dictionary(
        mean_hr_bpm, voltage_extremes, duration, num_beats, beats):
    """Creates a dictionary from all the needed metrics like
    mean heart rate, the voltage extremes, the duration of the ECG data,
    the number of heartbeats detected, and the times when the
    heartbeats occured

    Args:
        mean_hr_bpm: (int) average heart rate in BPM
        voltage_extremes: (tuple) tuple of the min and max voltage
        duration: (float) duration of ECG strip in ms
        num_beats: (int) the number of heartbeats detected
        beats: (array) the time values when heartbeats occured

    Returns:
        dictionary: a dictionary that organizes all these inputs

    """
    dictionary = {"mean_hr_bpm": str(mean_hr_bpm),
                  "voltage_extremes": str(voltage_extremes),
                  "duration": str(duration),
                  "num_beats": str(num_beats),
                  "beats": str(beats)}
    return dictionary


def short_file_name(file_name):
    """Determines a short file name to name the JSON file

    Args:
        file_name: The long file name of the input CSV file

    Returns:
        short_name: The shortened name of the CSV file
        so that the JSON is named the same thing

    """
    slash_index = file_name.rfind('/') + 1
    csv_index = file_name.rfind('.csv')
    short_name = file_name[slash_index:csv_index]
    return short_name


def output_to_json(file_name, dictionary):
    """Write the dictionary of values into a JSON file
    Makes a JSON file with the same name as the CSV data file

    Args:
        file_name: the long file name of the CSV. Will be
        shortened through a built the short_file_name function
        dictionary: the dictionary will all the data to be
        written to the JSON file.

    Returns:
        None

    """
    name_of_json = short_file_name(file_name)
    with open(name_of_json+'.json', 'w') as fp:
        json.dump(dictionary, fp, indent=4)

# Run the package below**************************************************


if __name__ == "__main__":
    Tk().withdraw()
    file_name = askopenfilename()
    # file_name = 'C:/Users/Howard Li/OneDrive/^2018 Fall/Software Design/' \
    #            'bme590hrm/test_data/test_data1.csv'
    ecg_data = read_ecg(file_name)
    is_enough_data(ecg_data)
    time_data = split_time_data(ecg_data)
    volt_data = split_volt_data(ecg_data)
    peaks = detect_peaks(volt_data, mph=0, mpd=10, edge='rising', show=False)
    voltage_extremes = find_volt_extreme(volt_data)
    is_volt_data_in_range(voltage_extremes)
    duration = find_time_duration(time_data)
    is_time_too_short(duration)
    num_beats = find_number_beats(peaks)
    is_peaks_detected(num_beats)
    beats = find_beat_times(time_data, peaks)
    user_specified_time = specify_time()
    mean_hr_bpm = find_avg_hr(beats, user_specified_time)
    dictionary = create_metrics_dictionary(
        mean_hr_bpm, voltage_extremes, duration, num_beats, beats)
    output_to_json(file_name, dictionary)
