'''
    Utility functions
    Author: Prateek Jaya Prakash {}
'''
import csv
import yaml
import os
import pandas as pd
import json

def read_yaml_file(yaml_file_path):
    """
    Method to read data from yaml file.

    Args:
        yaml_file_path (str): Input yaml file path.

    Returns:
        dict: Read data from file.

    Raises:
        ValueError: if error occurs in reading file.

    """
    try:
        if not os.path.isfile(yaml_file_path):
            print("Yaml file does not exist")
            #raise ValueError(f"File does not exist: {yaml_file_path}")

        yaml_data = None
        with open(yaml_file_path, "r") as yaml_file:
            try:
                yaml_data = yaml.load(yaml_file, Loader=yaml.Loader)
            except yaml.YAMLError as error:
                raise ValueError(error)
        return yaml_data
    except Exception as e:
        print(e)

def read_csv_table(filename, col_header):
    """
    Reads a CSV file and returns a dictionary of the data.

    Parameters:
    filename (str): the path to the CSV file
    col_header (str): the column header to use as the dictionary keys

    Returns:
    dict: a dictionary of the data, with the column header as the keys and the rows as the values
    """
    try:
        # Read the CSV file and store it in a dataframe
        df = pd.read_csv(filename)

        # Convert the column names in the dataframe to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Convert the col_header to lowercase
        col_header = col_header.lower()

        # Check if the col_header is present in the list of column names
        if col_header not in df.columns:
            raise ValueError(f"Column header '{col_header}' not found in the dataframe")

        # Remove duplicates from the dataframe and set the col_header as the index
        df = df[~df[col_header].duplicated(keep='first')]
        df = df.set_index(col_header)

        # Convert the dataframe to a dictionary and return it
        data_dict = df.to_dict('index')
        return data_dict
    except Exception as e:
        # Print an error message if any exception occurs
        print("An error occurred while reading the file:", e)