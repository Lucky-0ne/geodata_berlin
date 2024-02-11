import geopandas as gpd
import pandas as pd
from datetime import datetime, timedelta

def open_new_data(new_data_path, PLR_ID_column_name, encoding='ISO-8859-1'):
    """
    Open the new data file and return a DataFrame with the PLR_ID column renamed to 'PLR_ID'.

    :param new_data_path: The path to the new data file.
    :param PLR_ID_column_name: The name of the PLR_ID column in the new data file.
    :return: A DataFrame containing the new data.
    """
    # Open the new data file
    new_data = pd.read_csv(new_data_path, dtype={PLR_ID_column_name: str}, encoding=encoding)

    # Rename the PLR_ID column
    new_data.rename(columns={PLR_ID_column_name: 'PLR_ID'}, inplace=True)

    # Return the new data
    return new_data

def get_geodata(new_data, geojson_data):
    return geojson_data.merge(new_data, on='PLR_ID', how='left')

def extract_timestamps(df, timestamp_column_name, timestamp_format='mixed'):
    """
    Extract the year, month, day and hour from the timestamp column and add them as new columns to the DataFrame.

    :param df: The DataFrame containing the timestamp column.
    :param timestamp_column_name: The name of the timestamp column.
    :param timestamp_format: The format of the timestamp column.
    :return: The DataFrame with the new columns.
    """
    # Convert the timestamp column to datetime
    try:
        df[timestamp_column_name] = pd.to_datetime(df[timestamp_column_name], format=timestamp_format)
    except:
        print('Error: Timestamp column could not be converted to datetime.')
        return df

    # Extract the year, month, day and hour from the timestamp column and add them as new columns to the DataFrame
    df.loc[:, timestamp_column_name + '_year'] = df[timestamp_column_name].dt.year
    df.loc[:, timestamp_column_name + '_month'] = df[timestamp_column_name].dt.month
    df.loc[:, timestamp_column_name + '_day'] = df[timestamp_column_name].dt.day
    df.loc[:, timestamp_column_name + '_hour'] = df[timestamp_column_name].dt.hour

    # Return the DataFrame with the new columns
    return df