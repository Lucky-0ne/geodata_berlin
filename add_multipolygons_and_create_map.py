from tqdm import tqdm
tqdm.pandas()
from datetime import datetime, timedelta
from utils import *

# load new data to add geodata to
YEAR = 2022
new_data_path ='data/2022-2023_bikethefts/results/data_preprocessed/'
save_data_path = 'data/2022-2023_bikethefts/results/further_results/'
load_file_name = '2022-2023_bikethefts_preprocessed.csv'
save_file_name = f'{YEAR}_bikethefts_map.html'

df = open_new_data(new_data_path=new_data_path+load_file_name, PLR_ID_column_name='LOR', encoding='ISO-8859-1')

# TODO transform new data to effectively add geodata (e.g. group by PLR_ID and/or timestamp before adding geodata to each row)
df_ts = df.copy()
df_ts['theft_start'] = pd.to_datetime(df_ts['theft_start'])
df_ts.loc[:,'theft_start_year'] = df_ts['theft_start'].dt.year
df_ts.loc[:,'theft_start_month'] = df_ts['theft_start'].dt.month
df_ts.loc[:,'theft_start_day'] = df_ts['theft_start'].dt.day
df_ts.loc[:,'theft_start_hour'] = df_ts['theft_start'].dt.hour
# groupby PLR_ID and year
df_thefts_per_year = df_ts.groupby(['PLR_ID', 'theft_start_year']).size().reset_index(name='Bike_Thefts').sort_values('theft_start_year')
df_thefts_2022 = df_thefts_per_year[df_thefts_per_year['theft_start_year'] == YEAR]

# load geojson containing geodata
geojson_path = 'data/multipolygons/lor_planungsraeume_2021.geojson'
geojson_data = gpd.read_file(geojson_path)
## TODO check if transform is still nessecary (i don't think so)
# geojson_data = geojson_data.to_crs(3857)

# add geodata
explore_df = get_geodata(df_thefts_2022, geojson_data)

# fill NaNs with 0
explore_df['Bike_Thefts'] = explore_df['Bike_Thefts'].fillna(0)

# Transfrom to GeoDataFrame
explore_df = gpd.GeoDataFrame(explore_df)

map = explore_df.explore("Bike_Thefts", cmap="Reds")

map.save(save_data_path + save_file_name)

# Save as GeoJSON
# explore_df.to_file(new_data_path + load_file_name[:-4] + '.geojson', driver='GeoJSON')