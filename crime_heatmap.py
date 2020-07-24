import numpy as np
import folium
from folium import plugins
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import pandas as pd

# define all crime columns
crime_columns = [
'Break and Enter Commercial',
'Break and Enter Residential/Other',
'Mischief',
'Other Theft',
'Theft from Vehicle',
'Theft of Bicycle',
'Theft of Vehicle',
'Vehicle Collision or Pedestrian Struck (with Fatality)',
'Vehicle Collision or Pedestrian Struck (with Injury)',
]

# function to create a heatmap html page for 
# df - dataframe of change
# name - name of the file
def draw_crime_change_heatmap(df,name,max):
    station_arr = df[['Latitude','Longitude','Proportion of Change']].values
    m = folium.Map([49.2827,-123.1207], zoom_start=10)
    vancouver_zoning_geojson = './local-area-boundary.geojson'
    folium.GeoJson(
            vancouver_zoning_geojson,
            name='geojson',
            style_function=lambda feat: {
                'opacity': 0.3,
                'fillOpacity': 0,
                'weight': 2,
                'color': '#000000'
                }
            ).add_to(m)
    m.add_child(plugins.HeatMap(station_arr,radius=8))
    m.save(f'./{name}.html')

# function to create a heatmap html page for 
# df - dataframe of crime dataframe
# name - name of the file
def draw_crime_intensity_heatmap(df,name):
    station_arr = df[['Y','X']].values
    m = folium.Map([49.2827,-123.1207], zoom_start=10)
    vancouver_zoning_geojson = './local-area-boundary.geojson'
    folium.GeoJson(
     # vancouver_zoning_geojson = path to the json
            vancouver_zoning_geojson,
            name='geojson',
            style_function=lambda feat: {
                'opacity': 0.3,
                'fillOpacity': 0,
                'weight': 2,
                'color': '#000000'
                }
            ).add_to(m)
    m.add_child(plugins.HeatMap(station_arr,radius=8))
    m.save(f'./{name}.html')

# function to create all heatmap html pages for criminal intensity
def create_all_crime_change_heatmap():
    for i in range(400,2000,400):
        data2006 = pd.read_pickle(f'combined-data-2006-2011-bound{i}.zip')
        data2011 = pd.read_pickle(f'combined-data-2011-2016-bound{i}.zip')
        crimes2006 = data2006[crime_columns]
        crimes2011 = data2011[crime_columns]
        data2006['CRIMES_TOTAL_FLAT'] = crimes2006.sum(axis=1)
        data2011['CRIMES_TOTAL_FLAT'] = crimes2011.sum(axis=1)

        draw_crime_change_heatmap(data2006,f'crimes_change_2006_2011_bound{i}',i/200)
        draw_crime_change_heatmap(data2011,f'crimes_change_2011_2016_bound{i}',i/200)

# function to read the crime dataframe and create heatmaps from the function above
def create_all_crime_heatmap():
    df = pd.read_pickle('./crime_intensity.zip')
    df_group = df.groupby(['TAX_ASSESSMENT_YEAR'])
    for i in df_group.groups.keys():
        draw_crime_intensity_heatmap(df_group.get_group(i),f'crimes_intensity_{i}')

# function to preprocessed the crime dataset dataframe
def preprocess_proportional_inf(df):
    max_droped_rows = 20000
    for col in proportion_columns:
        n_inf = np.count_nonzero(np.isinf(df[col]))
        if n_inf is not 0:
            if n_inf > max_droped_rows:
                df = df.drop(col, axis=1)
            else:
                df = df[~np.isinf(df[col])]
    return df

# function to drop outliets out of crime dataset dataframe
def drop_outliers(df, column):
    q1, q3 = df[column].quantile([0.25, 0.75]).values
    iqr = q3 - q1
    lower_bound, upper_bound = q1 - iqr*3, q3 + iqr*3
    return df[(lower_bound < df[column]) & (df[column] < upper_bound)]

create_all_crime_heatmap()
