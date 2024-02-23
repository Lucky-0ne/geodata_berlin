import geopandas as gpd
import pandas as pd
import warnings

## general TODO's:
# - add further features to return_columns_map/shp files, e.g. size, geo-correct centroid, population, etc.
# - fix duplicate PLZs in the shapefile
# - fix duplicate PLR_NAME for "Schloßstraße" in the shapefile
# - revise class, method and parameter names
# - revise docstrings
# - add further functionalities, e.g. CT's "neighbourhood" idea, etc.

class LookupTableManager:
    def __init__(self, resolution_mode, map_by='ID'):
        """
        Initializes the lookup table manager by loading the shapefile data into memory.
        
        :param shapefile_path: Path to the shapefile repository.
        """

        self.resolution_mode = resolution_mode

        if resolution_mode == 'PLZ':
            # TODO fix duplicate PLZs in the shapefile
            lookup_table_df_duplicates = gpd.read_file('plz_shp/plz.shp')
            self.lookup_table_df = lookup_table_df_duplicates.drop_duplicates(subset='plz')
            if map_by == 'ID' or 'NAME':
                self.id_column = 'plz'
                # TODO add further features to return_columns_map/shp files, e.g. size, population, etc.
                self.return_columns_map = {'geometry': 'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'! (interchangeable for PLZ)")
            
        elif resolution_mode == 'LOR_BZR':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_bzr.shp')
            if map_by == 'ID':
                self.id_column = 'BZR_ID'
                self.return_columns_map = {'name':'BZR_NAME', 'geometry':'geometry'}
            elif map_by == 'NAME':
                self.id_column = 'BZR_NAME'
                self.return_columns_map = {'id':'BZR_ID', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")
            
        elif resolution_mode == 'LOR_PGR':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_pgr.shp')
            if map_by == 'ID':
                self.id_column = 'PGR_ID'
                self.return_columns_map = {'name':'PGR_NAME', 'geometry':'geometry'}
            elif map_by == 'NAME':
                self.id_column = 'PGR_NAME'
                self.return_columns_map = {'id':'PGR_ID', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")
            
        elif resolution_mode == 'LOR_PLR':
            # self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_plr.shp')
            # TODO fix duplicate PLR_NAME for "Schloßstraße" in the shapefile, then remove self.lookup_table_df declaration in the following if statements
            if map_by == 'ID':

                ### remove when duplicate todo is fixed
                self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_plr.shp')
                ###

                self.id_column = 'PLR_ID'
                self.return_columns_map = {'name':'PLR_NAME', 'geometry':'geometry'}
            elif map_by == 'NAME':

                ### remove when duplicate todo is fixed
                warnings.warn("For now the PLR IDs '06100102' & '04300414' ('Schloßstraße') will return NaN due to a pending bug fix!", UserWarning)
                lookup_table_df_duplicates = gpd.read_file('lor_shp_2021/lor_plr.shp')
                self.lookup_table_df = lookup_table_df_duplicates[~lookup_table_df_duplicates.duplicated(subset='PLR_NAME', keep=False)]
                ###

                self.id_column = 'PLR_NAME'
                self.return_columns_map = {'id':'PLR_ID', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")
            
        else:
            raise ValueError(f"Invalid Resolution Mode: '{resolution_mode}' - must be one of 'PLZ', 'LOR_BZR', 'LOR_PGR' or 'LOR_PLR'")
        
    def get_meta_data(self, input_df, id_col, exclude_column=[], df_type='geopandas'):
        """

        """
        if not isinstance(input_df, pd.DataFrame):
            raise ValueError(f"Input must be a pandas DataFrame, not a '{type(input_df)}'!")
        if not isinstance(id_col, str):
            raise ValueError(f"ID Column must be a string, not a '{type(id_col)}'!")
        if id_col not in input_df.columns:
            raise ValueError(f"ID Column '{id_col}' not found in input DataFrame!")
        if not isinstance(exclude_column, list):
            raise ValueError(f"exclude_column must be a list, not a '{type(exclude_column)}'!")
        if not all(isinstance(col, str) for col in exclude_column):
            raise ValueError(f"exclude_column must be a list of strings, containing 'geometry', 'name' or 'id'!")
        if not all(col in ['geometry', 'name', 'id'] for col in exclude_column):
            raise ValueError(f"exclude_column must be a list of strings, containing 'geometry', 'name' or 'id'!")
        if len(exclude_column) != len(set(exclude_column)):
            raise ValueError(f"exclude_column must not contain duplicate values!")

        # drop column from returned columns if it is in exclude_column
        if exclude_column:
            return_columns = [self.return_columns_map[col] for col in self.return_columns_map if col not in exclude_column]
        else:
            return_columns = list(self.return_columns_map.values())

        # Map IDs to meta data
        df = input_df.copy()
        for col in return_columns:
            df[col] = input_df[id_col].map(self.lookup_table_df.set_index(self.id_column)[col])

        # Convert the updated pandas DataFrame to a GeoDataFrame
        if df_type == 'geopandas':
            if 'geometry' in df.columns:
                df = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:25833")
            else:
                warnings.warn("Returning a geopandas DataFrame without a geometry column! It is recommended to use df_type='pandas' instead.", UserWarning)
                df = gpd.GeoDataFrame(df)
                # TODO could catch special case where geometry is already in input_df and return a geopandas DataFrame
        elif df_type == 'pandas':
            if 'geometry' in df.columns:
                warnings.warn("Returning a pandas DataFrame with a geometry column! It is recommended to use df_type='geopandas' instead.", UserWarning)
            else:
                pass
        else:
            raise ValueError(f"Invalid DataFrame Type: '{df_type}' - must be one of 'geopandas' or 'pandas'!")

        return df

############################ DEPRECATED #####################################

    def get_value(self, id, id_col='BZR_ID', return_col='geometry'):
        """
        Returns a value from the lookup table given a specific ID.
        
        :param id: The ID for which to find the corresponding value.
        :return: The value corresponding to the given ID, or None if not found.
        """
        result = self.lookup_table_df[self.lookup_table_df[id_col] == id][return_col]
        if not result.empty:
            return result.iloc[0]
        else:
            return None  # Or any appropriate default value
        
    def attach_geometries_to_dataframe(self, input_df, id_col, return_col='geometry'):
        """
        Attaches geometries to a pandas DataFrame based on an ID column, returning a GeoDataFrame.
        
        :param df: pandas DataFrame with an ID column.
        :param id_col: The column name in df that matches IDs in the lookup table.
        :return: A GeoDataFrame with original columns plus a geometry column, with the correct CRS.
        """

        if not isinstance(input_df, pd.DataFrame):
            raise ValueError(f"Input must be a pandas DataFrame, not a '{type(input_df)}'!")

        if not isinstance(id_col, str):
            raise ValueError(f"ID Column must be a string, not a '{type(id_col)}'!")
        elif id_col not in input_df.columns:
            raise ValueError(f"ID Column '{id_col}' not found in input DataFrame!")

        if return_col == 'geometry':
            # Map IDs to geometries
            df = input_df.copy()
            df['geometry'] = input_df[id_col].map(self.lookup_table_df.set_index(self.id_column)[return_col])

            # Convert the updated pandas DataFrame to a GeoDataFrame
            gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:25833")

            return gdf
        elif return_col == 'NAME':
            # Map IDs to names
            df = input_df.copy()
            df['NAME'] = input_df[id_col].map(self.lookup_table_df.set_index(self.id_column)[return_col])

            # check if input_df has a geometry column and if so, return a GeoDataFrame
            if 'geometry' in input_df.columns:
                gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:25833")
                return gdf
            else:
                return df
        else:
            raise ValueError(f"Invalid Return Column: '{return_col}' - must be one of 'geometry' or 'NAME'!")