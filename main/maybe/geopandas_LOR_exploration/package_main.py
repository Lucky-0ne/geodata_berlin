import geopandas as gpd

class LookupTableManager:
    def __init__(self, mode):
        """
        Initializes the lookup table manager by loading the shapefile data into memory.
        
        :param shapefile_path: Path to the shapefile repository.
        """

        if mode == 'PLZ':
            self.lookup_table_df = gpd.read_file('plz_shp/plz.shp')
            self.id_column = 'plz'
        elif mode == 'BZR_ID':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_bzr.shp')
            self.id_column = 'BZR_ID'
        elif mode == 'BZR_NAME':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_bzr.shp')
            self.id_column = 'BZR_NAME'
        elif mode == 'PGR_ID':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_pgr.shp')
            self.id_column = 'PGR_ID'
        elif mode == 'PGR_NAME':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_pgr.shp')
            self.id_column = 'PGR_NAME'
        elif mode == 'PLR_ID':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_plr.shp')
            self.id_column = 'PLR_ID'
        elif mode == 'PLR_NAME':
            self.lookup_table_df = gpd.read_file('lor_shp_2021/lor_plr.shp')
            self.id_column = 'PLR_NAME'
        else:
            raise ValueError(f"Invalid mode: '{mode}' - must be one of 'PLZ', 'BZR_ID', 'BZR_NAME', 'PGR_ID', 'PGR_NAME', 'PLR_ID', 'PLR_NAME!")
    
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
        
    def attach_geometries_to_dataframe(self, input_df, id_col='BZR_ID', return_col='geometry'):
        """
        Attaches geometries to a pandas DataFrame based on an ID column, returning a GeoDataFrame.
        
        :param df: pandas DataFrame with an ID column.
        :param id_col: The column name in df that matches IDs in the lookup table.
        :return: A GeoDataFrame with original columns plus a geometry column, with the correct CRS.
        """
        # Map IDs to geometries
        df = input_df.copy()
        df['geometry'] = input_df[id_col].map(self.lookup_table_df.set_index(self.id_column)[return_col])

        # Convert the updated pandas DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:25833")

        return gdf