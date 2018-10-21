import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def read_ecg(file_name):
    ecg_data = np.genfromtxt(file_name, delimiter=",")
    return ecg_data


if __name__ == "__main__":
    Tk().withdraw()
    file_name = askopenfilename()
    print(read_ecg(file_name))
