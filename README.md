# bme590hrm
This is my repo for the Heart Rate Monitor project

 Author: Howard Li: https://github.com/HL232/bme590hrm
 
 Version: 1.0
 
 License: GNU General Public License v3.0

## What's included in this repo:
 + `test_data` folder with the ECG data CSV files
 + `.gitignore` file for what to ignore when working with Git
 + `.travis.yml` file for setting up Travis CI
 + `Functional Block Diagram.dox` a functional block diagram (that's really just a list) that I used for this project
 + `HeartRateMonitor.py` This is the main python code. Simply run this file to run my project. This file includes all the functions and the logic for reading the ECG data sets. More on how it works later
 + `README.md` This document
 + `detect_peaks.py` This is the peak detection algorithm I used for this project. Original author: Marcos Duarte. Source code can be found here: http://nbviewer.jupyter.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb. Usage under MIT license. 
 + `requirements.txt` This is the requirements for setting up a virtual environment
 + `test_HeartRateMonitor.py` This includes all my unit tests. 
 + `test_data1.csv, unit_int_test_data1.csv, unit_int_test_data2.csv` Are basic CSV files I use in the unit tests. Should be downloaded into the same local folder as the unit test code when pulling the repo
 + `docs, make.bat, index.rst, conf.pu, and Makefile` were all added after Sphinx Quickstart tool on Pycharm. It's not generating the documentation and I don't know how to fix it. 

## How to run this project:
 WARNING: This program only works well for "nice" ECG datasets. 
 1. Clone this repo, or download the contents
 2. In your local python virtual environment (eg: Anaconda, Pycharm, Linux, etc) run the HeartRateMonitor.py python file.
 3. You will first be prompted to select a file. You need to select a CSV file with ECG data. 
 4. You will then be prompted to choose a time interval. Type this into your python terminal. 
 5. The script will run. It will calculate the average heart rate over the specified time interval, the minimum and maximum voltages points, the duration of the ECG strip, the number of heartbeats detected, and the times when these heartbeats occurred.
 6. These values are saved onto a dictionary, imported into a JSON file with the same name as the CSV data file you selected. The JSON file should save into the same folder as whereever you cloned this repo. 
 
## Detailed notes on code logic:
If you look at the `if __name__ == "__main__":` function, this is basically what is happening:
 1. tkinter package is used to allow the user to select which file to load into the program.
 2. The ECG data is read into a numpy array. EXCEPTIONS: Will raise a TypeError if you do not choose a CSV file
 3. EXCEPTION: Will raise a ValueError if the file you selected does not have at least 25 data points.
 4. The ECG numpy array is split into two separate arrays: the time data, and the voltage data. EXCEPTIONS: Will raise a TypeError if any of the data is non-numeric. Therefore the CSV file cannot contain any missing data or words
 5. Peaks are detected using the `detect_peaks` algorithm. The index locations of the peaks are saved.
 6. The voltage extremes (aka voltage min and max) are found. EXCEPTIONS: If the min or max voltage is outside the range of -5V to 5V, the program will prompt the user, asking to continue or not. This is because voltage data outside this range may not be good ECG data. User can choose to continue or not. Not a lethal error
 7. The duration of the ECG strip is determined using the last time data point. EXCEPTION: Will raise a ValueError if the ECG strip is not more than 5 seconds because this is not enough ECG data to make do good science.
 8. The number of beats detected is calculated. EXCEPTIONS: Will raise a ValueError if 0 heart beats are detected. 
 9. The time of when these beats occurs is calculated using the index values and the time array. 
 10. The program asks the user to specify a time for which to calculate average heart rate. If the user does not input an integer time, the default setting of 60 seconds is used.
 11. The mean heart rate is calculated over the user specifed time interval. 
 12. The above values in steps 7-12 are saved to a dictionary. The values are all stored as strings
 13. The dictionary is saved to a JSON file. The logic of how to name the JSON file is basically: Find the name of the CSV file, and save the JSON file as the same name. 


## What works and what doesn't:
 + `test_data1` - Works fine
 + `test_data2` - Works fine
 + `test_data3` - Detects too many heartbeat peaks
 + `test_data4` - Works fine
 + `test_data5` - Detects too many peaks
 + `test_data6` - Works fine
 + `test_data7` - Detects too many peaks
 + `test_data8` - Works fine
 + `test_data9` - Does not detect enough peaks
 + `test_data10` - Detects most peaks (still missing ~15% of heart beats)
 + `test_data11` - Too many peaks
 + `test_data12` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data13` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data14` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data15` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data16` - Works fine
 + `test_data17` - Works fine
 + `test_data18` - Works fine
 + `test_data19` - Works fine
 + `test_data20` - Works fine
 + `test_data21` - Works fine
 + `test_data22` - Works fine
 + `test_data23` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data24` - Code recognizes that this is probably not a good ECG dataset because it has a voltage over 5V. User can stop
 + `test_data25` - Only 1 heartbeat detected
 + `test_data26` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data27` - 0 heart beats detected (throws an Error because of this. No JSON file produced)
 + `test_data28` - throws an error, the time data is not all numeric. Maybe missing data or contains non-numbers
 + `test_data29` - throws an error, the time data is not all numeric. Maybe missing data or contains non-numbers
 + `test_data30` - throws an error, the time data is not all numeric. Maybe missing data or contains non-numbers
 + `test_data31` - throws an error, the time data is not all numeric. Maybe missing data or contains non-numbers
 + `test_data32` - Code works, but Code recognizes that this is probably not a good ECG dataset because it has a voltage over 5V. User can stop
 
 
## Future To do Items:
 + I CAN'T GET THE SPHINX DOCUMENTATION TO AUTO GENERATE DOCUMENTATION AGH
 + Make the heart beat detection/peak finding algorithm more robust
 + Handle missing data points in the ECG data set
 + Make the user inputs and user interface a bit more user friendly (maybe add GUIs and stuff)
 + Get the heart rate monitor to work for all the test data sets







 The original assignment is copied below:

# Heart Rate Monitor

Create a new repository--`bme590hrm`--in your individual space on GitHub, and make sure to add all instructors and teaching assistants as [CODEOWNERS](https://help.github.com/articles/about-codeowners/).

## Heart Rate Monitor: Functional Specifications
  + Read ECG data from a CSV file that will have lines with `time, voltage`.  Example data can be found in the `test_data/` directory in this assignment directory.  
  + The following data should be calculated and saved as keys in a Python dictionary called `metrics`:
    - `mean_hr_bpm`: estimated average heart rate over a user-specified number
      of minutes (can choose a default interval)
    - `voltage_extremes`: tuple containing minimum and maximum lead voltages
    - `duration`: time duration of the ECG strip
    - `num_beats`: number of detected beats in the strip
    - `beats`: numpy array of times when a beat occurred
  + Your `metrics` dictionary should be output as a [JSON](https://json.org/) file should be saved with the same name as the input CSV file that contains the values of all of your object attributes.  Note that there is a [json module](https://docs.python.org/3.6/library/json.html) that will make your life easier.

## Git Version Control Practices
  + Frequent and meaningful commits!  
    - Branches should be used for specific feature implementations, bug fixes, etc.  
    - Do not delete your branches after merging them into master. 
    - If you locally merge, use the `-no-ff` option so that we can audit your commit logs to see the merge operations.  (This will lead to a "messy" commit history, but something that we want to see for grading purposes.)
  + Project management Milestones \& Issues (with associated git commits), along with descriptive Labels.
  + Write a single function for each functional element of your code, and all function must have associated unit tests with complete coverage.
  + Feature branches merged into master (after passing unit tests with Travis CI).
  + Make sure that your project has a `README.md` file that describes how to run it, and also make sure that you associate a software license with your project (http://choosealicense.com/).  
  + Bonus - integrate a Travis [status badge](https://docs.travis-ci.com/user/status-images/) in your README that displays the status of test passage.
  + Create an annotated tag titled `v1.0.0` when your assignment is completed and ready to be graded.  Check out details on semantic versioning here: http://semver.org

## Python Code Expectations
* Utilize a virtual environment.
* Have Sphinx-friendly (https://pythonhosted.org/an_example_pypi_project/sphinx.html) docstrings for all methods.  
* Unit tests should exist in a separate file or directory of test files. 
* Achieve the functional specifications with passing unit tests.  Make sure that you include a test for writing the output JSON file.
* All methods should have well-defined input-action-output (as the unit tests will demand).
* There should be no "hard-coded" values in your methods.
* Adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) style. 
* Implement exception handling
* Gracefully terminate when the input file ends
* Create meaningful logs (e.g., `INFO` for assigning values to attributes, `WARNING` or `ERROR` for exceptions)

## Grading Criteria
* Effective version control usage
* Adequate unit test coverage and functional modularity
* Python style and docstrings
* Achieves functional specifications
* Works with all of the provided test data
* Extra features = bonuses!
