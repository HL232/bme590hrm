import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from detect_peaks import detect_peaks


def read_ecg(file_name):
    ecg_data = np.genfromtxt(file_name, delimiter=",")
    return ecg_data


def avg_hr(ecg_data, detected_peaks):
    time_array = ecg_data[:, 0][detected_peaks]  # returns the time in ms of when the peaks occurred
    max_time = time_array[-1]  # the time of the last peak
    num_beats = len(time_array)  # the number of beats in the array
    mean_hr_bpm = int(round(60/max_time*num_beats))
    return mean_hr_bpm


def volt_extreme(ecg_data):
    volt_data = ecg_data[:, 1]
    max_volt = max(volt_data)
    min_volt = min(volt_data)
    voltage_extremes = (min_volt, max_volt)
    return voltage_extremes


def time_duration(ecg_data):
    time_array = ecg_data[:, 0]
    duration = time_array[-1]
    return duration


def number_beats(detected_peaks):
    num_beats = len(detected_peaks)
    return num_beats


def beat_times(detected_peaks):
    beats = ecg_data[:, 0][detected_peaks]
    return beats


if __name__ == "__main__":
    Tk().withdraw()
    # **************************************************************Replace the file path with file_name in the future
    # file_name = askopenfilename()
    file_name = 'C:/Users/Howard Li/OneDrive/^2018 Fall/Software Design/bme590hrm/test_data/test_data1.csv'
    ecg_data = read_ecg(file_name)
    ind = detect_peaks(ecg_data[:, 1], mph=0, mpd=10, edge='rising', show=True)
    print(ind)
    print('The average heart rate is: ' + str(avg_hr(ecg_data, ind)))
    print('The voltage extremes are: ' + str(volt_extreme(ecg_data)))
    print('The time duration of the ECG strip is: ' + str(time_duration(ecg_data)) + 'ms')
    print('The number of beats in the strip is: ' + str(number_beats(ind)))
    print('The array of beat times is: ' + str(beat_times(ind)))
