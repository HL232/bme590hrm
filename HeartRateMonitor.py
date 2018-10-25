import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from detect_peaks import detect_peaks
import json

# Read the data ***********************************************


def read_ecg(file_name):
    if file_name.endswith(".csv"):
        ecg_data = np.genfromtxt(file_name, delimiter=",")
        return ecg_data
    elif not file_name.endswith(".csv"):
        raise TypeError("File is not a CSV file")


# Process the data *******************************************


def split_time_data(ecg_data):
    time_data = ecg_data[:, 0]
    return time_data


def split_volt_data(ecg_data):
    volt_data = ecg_data[:, 1]
    return volt_data


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


# Input is the beats from find_beat_times
def find_avg_hr(time_of_beats):
    max_time = time_of_beats[-1]  # the time of the last peak
    num_beats = len(time_of_beats)  # the number of beats in the array
    mean_hr_bpm = int(round(60/max_time*num_beats))
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


if __name__ == "__main__":
    Tk().withdraw()
    # ********************Replace the file path with file_name in the future
    # file_name = askopenfilename()
    file_name = 'C:/Users/Howard Li/OneDrive/^2018 Fall/Software Design/' \
                'bme590hrm/test_data/test_data1.csv'
    try:
        ecg_data = read_ecg(file_name)
    except TypeError:
        print("Please use a .csv file and try again")
        ecg_data = []
    time_data = split_time_data(ecg_data)
    volt_data = split_volt_data(ecg_data)
    peaks = detect_peaks(volt_data, mph=0, mpd=10, edge='rising', show=False)
    voltage_extremes = find_volt_extreme(volt_data)
    duration = find_time_duration(time_data)
    num_beats = find_number_beats(peaks)
    beats = find_beat_times(time_data, peaks)
    mean_hr_bpm = find_avg_hr(beats)
    dictionary = create_metrics_dictionary(
        mean_hr_bpm, voltage_extremes, duration, num_beats, beats)
    print(dictionary)
    output_to_json(file_name, dictionary)
