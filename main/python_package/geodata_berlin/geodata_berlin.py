import geopandas as gpd
import pandas as pd
import warnings

## general TODO's:
# - fix duplicate PLZs in the shapefile
# - fix duplicate PLR_NAME/BZR_NAME for "Schloßstraße"/"Heerstraße" in the shapefile
# - revise class, method and parameter names
# - revise docstrings
# - add further functionalities, e.g. CT's "neighbourhood" idea, etc.
# - summarise raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!") in one place
# - review exclude_column
# - reformat CRS of "districts" and "local districts" shapefiles from "EPSG:4326" to "EPSG:25833"

## big TODO:
# - strip all meta infos except for geometry, id and name from shapefiles and add the rest to a separate csv file
# --> then maybe create new meta data handler
## (discarded idea):
# - add further features to return_columns_map/shp files, e.g. size, geo-correct centroid, population, etc.

class LookupTableManager:

    def __init__(self, resolution_mode, map_by='ID'):
        """
        Initializes the lookup table manager by loading the shapefile data into memory.
        
        :param shapefile_path: Path to the shapefile repository.
        """

        data_path = 'geodata_berlin/data/'

        if resolution_mode == 'PLZ':
            if map_by in ['ID', 'NAME']:
                self.id_column = 'plz'
                self.return_columns_map = {'geometry': 'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'! (interchangeable for PLZ)")
            # TODO fix duplicate PLZs in the shapefile
            lookup_table_df_duplicates = gpd.read_file(data_path + 'plz_shp/plz.shp')
            self.lookup_table_df = lookup_table_df_duplicates.drop_duplicates(subset='plz')
            
        elif resolution_mode == 'LOR_PGR':
            self.lookup_table_df = gpd.read_file(data_path + 'lor_post2021_PGR/lor_prognoseraeume_2021.shp')
            if map_by == 'ID':
                self.id_column = 'PGR_ID'
                self.return_columns_map = {'LOR_PGR_name':'PGR_NAME', 'district_id':'BEZ', 'geometry':'geometry'}
            elif map_by == 'NAME':
                self.id_column = 'PGR_NAME'
                self.return_columns_map = {'LOR_PGR_id':'PGR_ID', 'district_id':'BEZ', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")

        elif resolution_mode == 'LOR_BZR':
            # self.lookup_table_df = gpd.read_file(data_path + 'lor_post2021_BZR/lor_bezirksregionen_2021.shp')
            # TODO fix duplicate BZR_NAME for "Heerstraße" in the shapefile, then remove self.lookup_table_df declaration in the following if statements
            if map_by == 'ID':

                ### remove when duplicate todo is fixed
                self.lookup_table_df = gpd.read_file(data_path + 'lor_post2021_BZR/lor_bezirksregionen_2021.shp')
                ###

                self.id_column = 'BZR_ID'
                self.return_columns_map = {'LOR_BZR_name':'BZR_NAME', 'district_id':'BEZ', 'geometry':'geometry'}
            elif map_by == 'NAME':

                ### remove when duplicate todo is fixed
                warnings.warn("For now the BZR IDs '042002' & '052005' ('Heerstraße') will return NaN due to a pending bug fix!", UserWarning)
                lookup_table_df_duplicates = gpd.read_file(data_path + 'lor_post2021_BZR/lor_bezirksregionen_2021.shp')
                self.lookup_table_df = lookup_table_df_duplicates[~lookup_table_df_duplicates.duplicated(subset='BZR_NAME', keep=False)]
                ###

                self.id_column = 'BZR_NAME'
                self.return_columns_map = {'LOR_BZR_id':'BZR_ID', 'district_id':'BEZ', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")
            
        elif resolution_mode == 'LOR_PLR':
            # self.lookup_table_df = gpd.read_file(data_path + 'lor_shp_2021/lor_plr.shp')
            # TODO fix duplicate PLR_NAME for "Schloßstraße" in the shapefile, then remove self.lookup_table_df declaration in the following if statements
            if map_by == 'ID':

                ### remove when duplicate todo is fixed
                self.lookup_table_df = gpd.read_file(data_path + 'lor_post2021_PLR/lor_planungsraeume_2021.shp')
                ###

                self.id_column = 'PLR_ID'
                self.return_columns_map = {'LOR_PLR_name':'PLR_NAME', 'district_id':'BEZ', 'geometry':'geometry'}
            elif map_by == 'NAME':

                ### remove when duplicate todo is fixed
                warnings.warn("For now the PLR IDs '06100102' & '04300414' ('Schloßstraße') will return NaN due to a pending bug fix!", UserWarning)
                lookup_table_df_duplicates = gpd.read_file(data_path + 'lor_post2021_PLR/lor_planungsraeume_2021.shp')
                self.lookup_table_df = lookup_table_df_duplicates[~lookup_table_df_duplicates.duplicated(subset='PLR_NAME', keep=False)]
                ###

                self.id_column = 'PLR_NAME'
                self.return_columns_map = {'LOR_PLR_id':'PLR_ID', 'district_id':'BEZ', 'geometry':'geometry'}
            else:
                raise ValueError(f"Invalid mapping type: '{map_by}' - must be one of 'ID' or 'NAME'!")
            
        elif resolution_mode == 'DISTRICTS':
            # TODO load transformed gdf directly
            lookup_table_df_EPSG4326 = gpd.read_file(data_path + 'districts/bezirksgrenzen.shp')
            self.lookup_table_df = lookup_table_df_EPSG4326.to_crs(epsg=25833)
            if map_by == 'ID':
                self.id_column = 'Gemeinde_s'
                self.return_columns_map = {'district_name':'Gemeinde_n', 'geometry':'geometry'}
            elif map_by == 'NAME':
                self.id_column = 'Gemeinde_n'
                self.return_columns_map = {'district_id':'Gemeinde_s', 'geometry':'geometry'}

        elif resolution_mode == 'LOCAL_DISTRICTS':
            # TODO data from before 2020 --> since then new local district "Schlachtensee"
            # TODO load transformed gdf directly
            lookup_table_df_EPSG4326 = gpd.read_file(data_path + 'local_districts/lor_ortsteile.shp')
            self.lookup_table_df = lookup_table_df_EPSG4326.to_crs(epsg=25833)
            if map_by == 'ID':
                self.id_column = 'spatial_na'
                self.return_columns_map = {'local_district_name':'OTEIL', 'district_name':'BEZIRK', 'geometry':'geometry'}
            elif map_by == 'NAME':
                self.id_column = 'OTEIL'
                self.return_columns_map = {'local_district_id':'spatial_na', 'district_name':'BEZIRK', 'geometry':'geometry'}

        else:
            raise ValueError(f"Invalid Resolution Mode: '{resolution_mode}' - must be one of 'PLZ', 'LOR_BZR', 'LOR_PGR', 'LOR_PLR', 'DISTRICTS' or 'LOCAL_DISTRICTS'!")
        
    def map_geodata(self, input_df, id_col, df_type='geopandas', calculate_size=True):
        """

        """
        if not isinstance(input_df, pd.DataFrame):
            raise ValueError(f"Input must be a pandas DataFrame, not a '{type(input_df)}'!")
        if not isinstance(id_col, str):
            raise ValueError(f"ID Column must be a string, not a '{type(id_col)}'!")
        if id_col not in input_df.columns:
            raise ValueError(f"ID Column '{id_col}' not found in input DataFrame!")
        if not (input_df[id_col].map(type) == str).all():
            raise ValueError(f"ID Column '{id_col}' must contain only string values!")

        # Map IDs to meta data
        df = input_df.copy()
        for column_name_in_returned_df, column_name_in_lookuptable in self.return_columns_map.items():
            df[column_name_in_returned_df] = input_df[id_col].map(self.lookup_table_df.set_index(self.id_column)[column_name_in_lookuptable])
        
        # Convert the updated pandas DataFrame to a GeoDataFrame
        if df_type == 'geopandas':
            if 'geometry' in df.columns:
                df = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:25833")
                if calculate_size: df['size_km2'] = round(df['geometry'].area / 1_000_000, 6)
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