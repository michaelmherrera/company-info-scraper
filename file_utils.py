import os
import pandas as pd
import datetime
import logging


def set_up_dataframe(input_file):
    """ Given input_file (a properly formatted csv) generate a pandas dataframe
    with additional columns to store the www. prefix and the domain.

    Parameters
    ----------
    input_file : path
        the path to the input csv file

    Returns
    -------
    pandas dataframe
        a dataframe containing the original information and, additional columns to store the www. prefix and the domain
    """
    


    
    df = pd.read_csv(input_file)
    index = len(df.columns)
    df.insert(index, 'www', 'www.')
    df.insert(index+1, 'domain', None)
    return df


def init(input_file, output_file):
    """Creates the dataframe from the input_file

    """
    df = set_up_dataframe(input_file)
    return df


def incremental_save(df, output_file, index):
    """Save an incremental copy of the dataframe as CSV in the temp folder

    """

    df.to_csv(output_file)
    logging.debug(f'Saved incremental progress. Next index: {index+1}')


def save(df, dir, file_name):
    """Saves dataframe df in the path specified by dir and file_name

    """
    path = os.path.join(dir, file_name)
    df.to_csv(path)
