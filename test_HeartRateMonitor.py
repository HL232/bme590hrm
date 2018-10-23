import pytest
from HeartRateMonitor import *
import numpy as np


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


'''
blahhh def test_find_number_beats():
    a = find_number_beats(detect_peaks(read_ecg('test_data1.csv')))
    b = 35
    assert a == b


def test_find_beat_times():
    a = find_beat_times(split_time_data(read_ecg('unit_int_test_data1.csv')),
    detect_peaks(read_ecg('test_data1.csv')))
    b = [ 0.214 1.028 1.842 2.631 3.419 4.208 5.025 5.681 6.675 7.517
 8.328 9.119 9.889 10.731 11.586 12.406 13.236 14.058 14.853 15.65
 16.439 17.264 18.131 18.956 19.739 20.536 21.306 22.092 22.906 23.719
 24.547 25.394 26.2 26.972 27.772]
    np.testing.assert_array_equal(a,b)


def find_avg_hr(time_of_beats):
    a = find_avg_hr(split_time_data(read_ecg('unit_int_test_data1.csv')))
    b = 76
    assert a == b
'''
