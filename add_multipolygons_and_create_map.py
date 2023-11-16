from tqdm import tqdm
tqdm.pandas()
from utils import *

# load new data to add geodata to
YEAR = 2023
new_data_path ='data/2022-2023_bikethefts/'
load_file_name = '2022-2023_bikethefts_preprocessed.csv'
save_file_name = f'{YEAR}_bikethefts_map.html'

df = open_new_data(new_data_path=new_data_path+load_file_name, PLR_ID_column_name='LOR', encoding='ISO-8859-1')

# TODO transform new data to effectively add geodata (e.g. group by PLR_ID and/or timestamp before adding geodata to each row)
# groupby PLR_ID and year
df_thefts_per_year = df.groupby(['PLR_ID', 'Year']).size().reset_index(name='Bike_Thefts').sort_values('Year')
df_thefts_2022 = df_thefts_per_year[df_thefts_per_year['Year'] == YEAR]

# load geojson containing geodata
geojson_path = 'data/multipolygons/lor_planungsraeume_2021.geojson'
geojson_data = gpd.read_file(geojson_path)
## TODO check if transform is still nessecary (i don't think so)
# geojson_data = geojson_data.to_crs(3857)

# add geodata
explore_df = get_geodata(df_thefts_2022, geojson_data)

# Transfrom to GeoDataFrame
explore_df = gpd.GeoDataFrame(explore_df)

map = explore_df.explore("Bike_Thefts", cmap="Reds")

map.save(new_data_path + save_file_name)

# Save as GeoJSON
# explore_df.to_file(new_data_path + load_file_name[:-4] + '.geojson', driver='GeoJSON')