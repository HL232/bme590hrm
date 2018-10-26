import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from detect_peaks import detect_peaks
import json

# Read the data ***********************************************


def is_csv(file_name):
    if file_name.endswith(".csv"):
        return True
    elif not file_name.endswith(".csv"):
        raise TypeError("File is not a CSV file")
    return False


def read_ecg(file_name):
    if is_csv(file_name):
        ecg_data = np.genfromtxt(file_name, delimiter=",")
        return ecg_data


def is_data_not_float(data):
    # Tests that the data is all float data. Returns True is nan exists
    # This will also determine if volt_data and time_data are the same length
    data_good = any(np.isnan(t) for t in data)
    return data_good


def is_enough_data(data):
    if len(data) < 25:
        raise ValueError("You need more than 25 data points")


def split_time_data(ecg_data):
    time_data = ecg_data[:, 0]
    if is_data_not_float(time_data):
        raise TypeError('Time data is not all numeric')
    else:
        return time_data


def split_volt_data(ecg_data):
    volt_data = ecg_data[:, 1]
    if is_data_not_float(volt_data):
        raise TypeError('Voltage data is not all numeric')
    else:
        return volt_data

# Process the data *******************************************


def yes_no(from_input):
    answer = from_input
    while answer not in ("yes", "no"):
        answer = input("Enter yes or no: ")
        if answer == "yes":
            return
        elif answer == "no":
            raise SystemExit(0)
        else:
            print("Please enter yes or no.")


def is_volt_data_in_range(voltage_extremes):
    if voltage_extremes[0] < -5:
        stop_prompt = input('Voltage below -5V detected. '
                            'This probably is not good data.'
                            ' Continue? yes/no')
        yes_no(stop_prompt)
    elif voltage_extremes[1] > 5:
        stop_prompt = input('Voltage above 5V detected. '
                            'This probably is not good data.'
                            ' Continue? yes/no')
        yes_no(stop_prompt)


def is_time_too_short(duration):
    if duration < 5:
        raise ValueError("You need more than 5 seconds of ECG data")


def is_peaks_detected(num_beats):
    if num_beats == 0:
        raise ValueError("No heart beats detected in dataset")


def find_volt_extreme(volt_data):
    max_volt = max(volt_data)
    min_volt = min(volt_data)
    voltage_extremes = (min_volt, max_volt)
    return voltage_extremes


def find_time_duration(time_data):
    duration = time_data[-1]
    return duration


def find_number_beats(detected_peaks):
    num_beats = len(detected_peaks)
    return num_beats


# returns the time in ms of when the peaks occurred
def find_beat_times(time_data, detected_peaks):
    beats = time_data[detected_peaks]
    return beats


def specify_time():
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
    dictionary = {"mean_hr_bpm": str(mean_hr_bpm),
                  "voltage_extremes": str(voltage_extremes),
                  "duration": str(duration),
                  "num_beats": str(num_beats),
                  "beats": str(beats)}
    return dictionary


def short_file_name(file_name):
    slash_index = file_name.rfind('/') + 1
    csv_index = file_name.rfind('.csv')
    short_name = file_name[slash_index:csv_index]
    return short_name


def output_to_json(file_name, dictionary):
    name_of_json = short_file_name(file_name)
    with open(name_of_json+'.json', 'w') as fp:
        json.dump(dictionary, fp, indent=4)

# Run the package below**************************************************


if __name__ == "__main__":
    Tk().withdraw()
    # ********************Replace the file path with file_name in the future
    # file_name = askopenfilename()
    file_name = 'C:/Users/Howard Li/OneDrive/^2018 Fall/Software Design/' \
                'bme590hrm/test_data/test_data1.csv'
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
