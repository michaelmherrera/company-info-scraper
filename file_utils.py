import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import datetime
import logging

TEMP = "temp-saves"


def get_file_selections():
    """Prompts the user for the input file, output file and logging file

    """
    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename(title="Select input file")
    file_root = os.path.splitext(os.path.basename(input_file))[0]
    default_output = file_root + '_output.csv'
    output_file = filedialog.asksaveasfilename(
        title="Name output file", defaultextension='.csv', initialfile=default_output, filetypes=[('CSV (Comma delimited)', '.csv')])
    #Default log name is [YYYY-mm-dd_HH-MM-SS]_log.txt (EX: 2020-04-22_21-53-16_log.txt for April 20, 2020 at 9:53 PM and 16 seconds)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    default_log = '{}_{}_log.txt'.format(timestamp, file_root)
    log_file = filedialog.asksaveasfilename(
        title="Name log file", defaultextension='.txt', initialfile=default_log, filetypes=[('Text file', '.txt')])
    return input_file, output_file, log_file


def set_up_dataframe(input_file):
    """Given path to a csv, sets up the dataframe

    Given the path to a csv file, sets up a dataframe from the 
    file and adds the fields 'www' and 'domain' at the end

    """
    df = pd.read_csv(input_file)
    index = len(df.columns)
    df.insert(index, 'www', 'www.')
    df.insert(index+1, 'domain', None)
    return df


def init(input_file, save_dir):
    """Creates the dataframe from the input_file and generates a temp save directory within save_dir.

    """
    global TEMP
    temp_path = os.path.join(save_dir, TEMP)
    os.mkdir(temp_path)
    df = set_up_dataframe(input_file)
    return df


def incremental_save(df, save_dir, output_file, index):
    """Save an incremental copy of the dataframe as CSV in the temp folder

    """

    global TEMP
    temp_file = "INCREMENTAL_SAVE_0-{}_{}.csv".format(index, output_file)
    path = os.path.join(save_dir, TEMP)
    save(df, path, temp_file)
    print("Saved incremental progress. Next index: {}".format(index+1))


def save(df, dir, file_name):
    """Saves dataframe df in the path specified by dir and file_name

    """
    path = os.path.join(dir, file_name)
    df.to_csv(path)
