import pytest
from HeartRateMonitor import *
import numpy as np

file_name = 'test_data1.csv'
ecg_data = read_ecg(file_name)
time_data = split_time_data(ecg_data)
volt_data = split_volt_data(ecg_data)
peaks = detect_peaks(volt_data, mph=0, mpd=10, edge='rising', show=False)
voltage_extremes = find_volt_extreme(volt_data)
duration = find_time_duration(time_data)
num_beats = find_number_beats(peaks)
beats = find_beat_times(time_data, peaks)
mean_hr_bpm = find_avg_hr(beats)


def test_read_ecg():
    a = read_ecg('unit_int_test_data1.csv')
    b = np.array([[1, 6], [2, 7], [3, 8], [4, 9], [5, 10]])
    np.testing.assert_array_equal(a, b)


def test_split_time_data():
    a = split_time_data(read_ecg('unit_int_test_data1.csv'))
    b = np.array([1, 2, 3, 4, 5])
    np.testing.assert_array_equal(a, b)


def test_split_volt_data():
    a = split_volt_data(read_ecg('unit_int_test_data1.csv'))
    b = np.array([6, 7, 8, 9, 10])
    np.testing.assert_array_equal(a, b)


def test_find_volt_extreme():
    a = find_volt_extreme(split_volt_data(read_ecg('unit_int_test_data1.csv')))
    b = (6, 10)
    assert a == b


def test_find_time_duration():
    a = find_time_duration(split_time_data(
        read_ecg('unit_int_test_data1.csv')))
    b = 5
    assert a == b


def test_find_number_beats():
    a = num_beats
    b = 35
    assert a == b


def test_find_beat_times():
    a = beats[1]
    b = 1.028
    assert a == b


def test_find_avg_hr():
    a = mean_hr_bpm
    b = 76
    assert a == b


def test_create_metrics_dictionary():
    a = create_metrics_dictionary(1, 2, 3, 4, 5)
    b = {"mean_hr_bpm": '1',
         "voltage_extremes": '2',
         "duration": '3',
         "num_beats": '4',
         "beats": '5'}
    assert a == b


def test_short_file_name():
    a = short_file_name('@64fkndnkec%2mo82Fje/ adlkfj c/ihopetopass.csv')
    b = 'ihopetopass'
    assert a == b


def test_output_to_json():
    dict = {
        'a': '1',
        'b': '2',
        'c': '3'
    }
    a = output_to_json('/unit_test.csv', dict)
    with open('unit_test.json') as f:
        b = json.load(f)
    assert dict == b
