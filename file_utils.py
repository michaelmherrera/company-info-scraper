import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd

TEMP = "temp-saves"

def get_file_selections():
    """Prompts the user for the input file, save directory, and output filename

    """
    root = tk.Tk()
    root.withdraw()
    input("Press enter when ready to select input file...")
    input_file = filedialog.askopenfilename(title="Select input file")
    input("Press enter when ready to select an empty folder to store saved files...")
    save_dir = filedialog.askdirectory()
    output_file = input("Enter a name for the output file")
    return input_file, save_dir, output_file

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
    temp_file = "INCREMENTAL_SAVE_0-{}_{}.csv".format(index)
    path = os.path.join(save_dir, TEMP)
    save(df, path, temp_file)
    print("Saved incremental progress. Next index: {}".format(index+1))

def save(df, dir, file_name):
    """Saves dataframe df in the path specified by dir and file_name
    
    """
    path = os.path.join(dir, file_name)
    df.to_csv(path)