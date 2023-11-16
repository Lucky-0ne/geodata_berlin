import geopandas as gpd
import pandas as pd

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